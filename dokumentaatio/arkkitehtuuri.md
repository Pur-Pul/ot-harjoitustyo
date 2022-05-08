# Basic functionality
## Drawing and animating the clouds
When the application is started, a cloud is immediately generated and drawn.  
When the user clicks the "generate a new cloud" button, a new cloud is generated and drawn to replace the old.  
The animate button initiates a loop, whcih uses the WindSimulation algorithm to slightly change the cloud frame by frame.  
Each frame is drawn before the next is generated.  
```mermaid
sequenceDiagram
Main->>+GUI: GUI()
Main->>GUI: mainloop()
GUI->>+Cloud: Node(root_coordinates, cloud_table)
GUI->>+GUI: draw_cloud(cloud_table)
GUI->>+GUI: animate_cloud(frame_count)
GUI->>+Simulation: WindSimulation(cloud_table)
GUI->>+Simulation: simulate()
Simulation-->>-GUI: new_cloud_table
GUI-->>-GUI: draw_cloud(new_cloud_table)
```
