import matplotlib.pyplot as plt
from collections import deque

def setup_plot(window_size=500):
    plt.ion()
    fig, ax = plt.subplots()
    ax.set_title("Real-Time Bioelectric Signal")
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Voltage (V)") 
    
    line, = ax.plot([], [], lw=2)
    
    ax.set_xlim(-5, window_size)
    ax.set_ylim(-5, 5) 
    
    return fig, ax, line, deque(maxlen=window_size), deque(maxlen=window_size)

def update_plot(fig, ax, line, x_data, y_data, new_x, new_y):
    x_data.append(new_x)
    y_data.append(new_y)
    
    line.set_data(x_data, y_data)
    
    if new_x > 500:
        ax.set_xlim(new_x - 500, new_x)
        
    # Auto-Scale Y-Axis (Voltage)
    current_max = max(y_data) if y_data else 0
    current_limit = ax.get_ylim()[1]
    
    if current_max > current_limit * 0.9:
        ax.set_ylim(0, current_max * 1.2)
    elif current_max < current_limit * 0.3 and current_limit > 5:
        ax.set_ylim(0, max(5, current_max * 1.2))

