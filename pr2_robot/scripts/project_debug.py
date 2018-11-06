#!/usr/bin/env python

# Import modules
import numpy as np
import sklearn
from sklearn.preprocessing import LabelEncoder
import pickle
from sensor_stick.srv import GetNormals
from sensor_stick.features import compute_color_histograms
from sensor_stick.features import compute_normal_histograms
from visualization_msgs.msg import Marker
from sensor_stick.marker_tools import *
from sensor_stick.msg import DetectedObjectsArray
from sensor_stick.msg import DetectedObject
from sensor_stick.pcl_helper import *

import rospy
import tf
from geometry_msgs.msg import Pose
from std_msgs.msg import Float64
from std_msgs.msg import Int32
from std_msgs.msg import String
from pr2_robot.srv import *
from rospy_message_converter import message_converter
import yaml
import pcl

# Helper function to get surface normals
def get_normals(cloud):
    get_normals_prox = rospy.ServiceProxy('/feature_extractor/get_normals', GetNormals)
    return get_normals_prox(cloud).cluster

# Helper function to create a yaml friendly dictionary from ROS messages
def make_yaml_dict(test_scene_num, arm_name, object_name, pick_pose, place_pose):
    yaml_dict = {}
    yaml_dict["test_scene_num"] = test_scene_num.data
    yaml_dict["arm_name"]  = arm_name.data
    yaml_dict["object_name"] = object_name.data
    yaml_dict["pick_pose"] = message_converter.convert_ros_message_to_dictionary(pick_pose)
    yaml_dict["place_pose"] = message_converter.convert_ros_message_to_dictionary(place_pose)
    return yaml_dict

# Helper function to output to yaml file
def send_to_yaml(yaml_filename, dict_list):
    data_dict = {"object_list": dict_list}
    with open(yaml_filename, 'w') as outfile:
        yaml.dump(data_dict, outfile, default_flow_style=False)

# function to load parameters and request PickPlace service
def pr2_mover(object_list):

    #  Initialize variables
    test_scene_num = Int32()
    object_name = String()
    arm_name = String()
    pick_pose = Pose()
    place_pose = Pose()
    obj_list_dict = {}
    dropbox_dict = {}
    # TODO: Get/Read parameters
    test_scene_num.dta = rospy.get_param('/test_scene_num')
    object_list_param = rospy.get_param('/object_list')
    dropbox_param = rospy.get_param('/dropbox')
    # TODO: Parse parameters into individual variables
    for i in range(len(object_list_param)):
        obj_list_dict[object_list_param[i]['name']] = obj_list_dict[object_list_param[i]['group']]
    print(obj_list_dict)

    for data in dropbox_param:
        dropbox_dict[data['group']] = dropbox_data(data['position'], data['name'])
    print(dropbox_dict)
    '''
    # TODO: Rotate PR2 in place to capture side tables for the collision map

    # TODO: Loop through the pick list

        # TODO: Get the PointCloud for a given object and obtain it's centroid

        # TODO: Create 'place_pose' for the object

        # TODO: Assign the arm to be used for pick_place

        # TODO: Create a list of dictionaries (made with make_yaml_dict()) for later output to yaml format

        # Wait for 'pick_place_routine' service to come up
        rospy.wait_for_service('pick_place_routine')

        try:
            pick_place_routine = rospy.ServiceProxy('pick_place_routine', PickPlace)

            # TODO: Insert your message variables to be sent as a service request
            resp = pick_place_routine(TEST_SCENE_NUM, OBJECT_NAME, WHICH_ARM, PICK_POSE, PLACE_POSE)

            print ("Response: ",resp.success)

        except rospy.ServiceException, e:
            print "Service call failed: %s"%e

    # TODO: Output your request parameters into output yaml file
    '''


if __name__ == '__main__':

    # TODO: ROS node initialization
    rospy.init_node('object_recognise', anonymous=True)
    # TODO: Create Subscribers
    pcl_sub = rospy.Subscriber("/pr2/world/points", pc2.PointCloud2, pcl_callback, queue_size=1)
    # TODO: Create Publishers
    #pcl_data_pub = rospy.Publisher("/pcl_data", PointCloud2, queue_size=1)
    
    pcl_objects_pub = rospy.Publisher("/pcl_objects", PointCloud2, queue_size=1)
    pcl_table_pub = rospy.Publisher("/pcl_table", PointCloud2, queue_size=1)
    pcl_cluster_pub = rospy.Publisher("/pcl_cluster", PointCloud2, queue_size=1)
    # object_markers_pub = rospy.Publisher("/object_markers", Marker, queue_size=1)
    # detected_objects_pub = rospy.Publisher("/detected_objects", DetectedObjectsArray, queue_size=1)
    
    '''
    # TODO: Load Model From disk
    # model = pickle.load(open('model.sav', 'rb'))
    # clf = model['classifier']
    # encoder = LabelEncoder()
    # encoder.classes_ = model['classes']
    # scaler = model['scaler']
    '''
    # Initialize color_list
    get_color_list.color_list = []
    # TODO: Spin while node is not shutdown
    while not rospy.is_shutdown():
        rospy.spin()