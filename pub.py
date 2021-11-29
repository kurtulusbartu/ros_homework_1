import rospy
from turtlesim.msg import Pose
from std_msgs.msg import String
from geometry_msgs.msg import Twist, Vector3
import sys
from turtlesim.srv import *

twist = Twist()

def usage():
    return "%s [circle/square]"%sys.argv[0]

class TurtleBot:
    
    def __init__(self):
        rospy.init_node("pubb", anonymous=True)
        self.pub = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size=1000)
        self.sub = rospy.Subscriber("/turtle1/pose", Pose, self.update_pose)
        self.pose = Pose()
        self.rate = rospy.Rate(10)
        self.twist = Twist()

    def update_pose(self, data):
        self.pose = data
        self.pose.x = round(self.pose.x,4)
        self.pose.y = round(self.pose.y,4)
        print(data)

    def euclidean_distance(self, goal_pose):
        return ((goal_pose[0] - self.pose.x)**2+(goal_pose[1] - self.pose.y)**2)**(1/2)
    
    def square(self):

        distance_tolerance = 0.1

        while self.pose.x == 0:

            self.twist.linear.x = 0
            self.twist.linear.y = 0
        
        x = self.pose.x
        y = self.pose.y
        goal_poses = [[x+5, y],[x+5, y+5],[x, y+5],[x, y]]

        print(goal_poses)
        for set in range(0,4):
            while self.euclidean_distance(goal_poses[set]) >= distance_tolerance:

                if set == 0:
                    twist.linear.x = 2.5
                    twist.linear.y = 0
                    twist.linear.z = 0
                    twist.angular.x = 0
                    twist.angular.y = 0
                    twist.angular.z = 0

                if set == 1:
                    twist.linear.x = 0
                    twist.linear.y = 2.5
                    twist.linear.z = 0
                    twist.angular.x = 0
                    twist.angular.y = 0
                    twist.angular.z = 0

                if set == 2:
                    twist.linear.x = -2.5
                    twist.linear.y = 0
                    twist.linear.z = 0
                    twist.angular.x = 0
                    twist.angular.y = 0
                    twist.angular.z = 0
                
                if set == 3:
                    twist.linear.x = 0
                    twist.linear.y = -2.5
                    twist.linear.z = 0
                    twist.angular.x = 0
                    twist.angular.y = 0
                    twist.angular.z = 0

                self.pub.publish(twist)
                self.rate.sleep()
            
        twist.linear.x = 0
        twist.linear.y = 0
        self.pub.publish(twist)

        rospy.spin()
        
    def circle(self):

        twist = Twist()
            
        while not rospy.is_shutdown():
            twist.linear.x = 2.5
            twist.linear.y = 0
            twist.linear.z = 0
            twist.angular.x = 0
            twist.angular.y = 0
            twist.angular.z = 1

            self.pub.publish(twist)

if __name__ == "__main__":
    try:
        if len(sys.argv) == 2:
            command = str(sys.argv[1])
        else:
            print(usage())
            sys.exit(1)
        
        bot = TurtleBot()
        if command == "circle":
            bot.circle()
        if command == "square":
            bot.square()
    except rospy.ROSInterruptException:
        pass
