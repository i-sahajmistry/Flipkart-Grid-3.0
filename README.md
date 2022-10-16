# **Flipkart GRiD 3.0 Robotics Challenge**
## _Created a Centerally Monitered Parcel Sortation System_ 
<img src="/Images/Flipkart-logo.png" alt="Flipkart-logo" width="150"/>

**Problem Statement:** To develop central monitoring/navigation system (such as a camera or multiple cameras) should be used to understand the arena and the position of the robots and instruct robots on actions to be taken.

#### Bot Specifications
- Each bot is to fit within 6x6 inch square
- Each bot has a tray on top to carry 20x20x20 mm cube (approximate size)
- Tray has the ability to flip to drop items in chute
- No sensors for navigation/object detection to be mounted on the robot

The robot can only be touched by the operator when it is in the Induction zone

## **Round 1**

### Arena
<img src="/Images/Round1_Arena.png" alt="Arena-Round1" width="700"/>

#### Objectives (Relay race - 4 Robots)
- Each robot has a package on top
- Start positions are S1, S2, S3 & S4
- Bot from S1 is expected to go to D1, Bot from S2 is expected to go to D2 and so on...
- On start - Bot in the S1 location is expected to go to D1
- On reaching D1 it should drop the item beyond the wall
- Once the bot comes back to S1 (Completely inside S1 square), only then Bot from S2 can start
- Race is over when S4 robot comes back to its square after dropping the parcel

## **Round 2 And Finals**

### Arena
<img src="/Images/Round2_Arena.png" alt="Arena-Round2" width="700"/>

#### Objectives (Package Sortation)
- A list of packages will be given as part of the competition (Sample Sheet)
- The list will have a randomized list of Induct Station - Package ID - Destinations
- Packages to the same destination must be colored with the same color4. Only one package to be loaded on the Robot at a time
- You must decide which destinations are mapped to which chutes
- Two operators are needed - One at each induct zone
- You can decide the number of robots you plan to use
- Packages can be loaded onto bots only once bots are within the induct zones
- Bots need to move and drop off packages inside the chutes
- Competition is over when all packages are delivered or when 10 mins are up

##### _Sample Sheet_
| Package Id | Induct Station | Destination |
| ------ | ------ | ------ |
| FKMP0001 | 1 | Destination 1 |
| FKMP0002 | 2 | Destination 2 |
| FKMP0003 | 3 | Destination 3 |
| FKMP0004 | 4 | Destination 4 |

There would be a random distribution of
- Packages to destinations
- Packages to induct stations


## **Our Solution**

### About Bot
<img src="/Images/Bot1.JPG" alt="BOT1" width="450"/> <img src="/Images/Bot2.JPG" alt="BOT2" width="450"/>


> Bot was designed on solid works.
> CNC machine was used to cut acrylic sheets which were used to create chassis. 
> Parcel holding tray, tray stand and cover hood were 3D printed.

##### Components used

- [Micro-controller: NodeMCU ESP8266](https://robu.in/product/nodemcu-cp2102-board/): Used this specific micro-controller because has integrated WIFI module.
- [LiPo Battery](https://robu.in/product/orange-1500mah-2s-25c-7-4-v-lithium-polymer-battery-pack-li-po/): Rechargable long lasting battery.
- [Motor Driver L298N](https://robu.in/product/l298-based-motor-driver-module-2a/): Standard Motor Driver being used.
- [Servo Motor: Tower Pro SG90](https://robu.in/product/towerpro-sg90-9g-mini-servo-9-gram/): To throw parcel in chute.
- [N20 Moters with Encoders](https://robu.in/product/n20-12v-140rpm-micro-metal-gear-motor-with-encoder/): Encoders are used to make moton of bot straight.
- [Tyres](https://robu.in/product/3pi-miniq-car-wheel-tyre-42mm-n20-dc-gear-motor-wheel/): Tyres compitable with N20 motors.

##### Connections
Moter Driver -- Battery: Power Moter driver (Moter driver powers other components).
N20 Motor -- Motor Driver: For power and speed of rotation of motors.
N20 Motor -- NodeMCU: For reading output of encoder.
Moter Driver -- NodeMCU: Supply power and recieve speed for motors.
Servo Motor -- NodeMCU: To throw parcels.

##### Communication technique
Using python, a socket server was created to perticular port(which can be changed while running). This server was created on hotspot of the hosting device. Each of 4 NodeMCUs were a client trying to connect at different ports. Once a connection is created, messages can be transfered from client to server and server to client till the connection closes. We have used server to client message only.

##### Message
The message sent from server to client is a string consisting of 11 letters(Numbers). For Eg. "10101231231". To decrept the message let's break the message into 5 parts i.e. "10", "10", "123", "123", and "1". The first and second part tells about the direction of rotation of left and right side motors respectively. "10" means forward, "01" means reverse and "11"/"00" means stop. The "1" is high-voltage/1 to the specific terminal and "0" is low-voltage/0 to other terminal of motor. The third and forth parts tells about the speed of left and right motors respectively. "000" is zero speed and "255" is higest speed. The last part tells about the servo positioin. "1" is down and "0" is up.


##### Task of NodeMCU 
_{File path: /MicroController/MicroController.ion}_ </break>
1. Recieves message from server and decrepts it.
2. Gets the rotation of both sides of motors and calculates difference.
3. Using the speed from message and difference from encoder, it comes up with final speeds for both motors.
4. The final speeds are the sent to motor driver.
5. Waits for next message.
6. Goto 1.


##### Task of Python Script 
_{File path: /Round 1/winner1.py and /Round 2/main.py}_ </break>
1. Recieves input from camera using OpenCV.
2. Detects the position and direction of motion of all the bots (bots have aruco markers on top). _{implementation: /Round 2/utils.py}_
3. According to position and destination, the speed of both sides of motor are determined using a function.
4. This speed is then sent to the client (bot) over the socket server.
5. Bot moves.
6. GoTo 1.


<img src="/Images/Control Diagram.png" alt="Arena-Round2" width="900"/>

> Control Diagram of our Solution
