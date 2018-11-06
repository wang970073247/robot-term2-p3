
## Project: Kinematics Pick & Place

The goal of this project is to write code to use pr2 to recognise objects:

* Filtering and RANSAC plane fitting implemented.
* Clustering for segmentation implemented. 
* Object recognition implemented.

[//]: # (Image References)

[image1]: ./images/normal1.png
[image2]: ./images/normal2.png
[image3]: ./images/normal3.png
[image4]: ./images/recognise1.png
[image5]: ./images/recognise2.png
[image6]: ./images/recognise3.png
[image7]: ./images/train1.png
[image8]: ./images/train2.png
[image9]: ./images/train3.png
[image10]: ./images/show.png
[image11]: ./images/noise.png

---

![alt text][image10]

### Filtering and RANSAC plane fitting implemented.

---
* The original point cloud contains a lot of noise as figure below.

![alt text][image11]

#### step1:   Apply a Voxel Grid Downsampling
The code in pr2_robot/scripts/project_template.py between the lines 61-66

#### step2:   Apply the Statistical Outlier Removal Filter
As for this Filter, i tried many times for better paraments, it appers good 
when i Set the number of neighboring points to 4 and threshold scale factor to 0.01 to analyze for any given point. Just as the code between the lines
67-73.

#### step3:   Apply Two PassThrough Filter, one over Z one over X
The delailed is lied in the code between the lines 74-89, as for the parameters, you should try many times to find the better one.

#### step4:   Apply the RANSAC Plane Segmentation and Extract inliers and outliers
The code lies between lines 90-101, as for the parameter max_distance, 0.01 or 0.015 is good.

After that we can get point cloud about the table and the objects on the table separately.As the two pictures showed below:

pic1:The table point cloud
![alt text][image1]


pic2:The objects point cloud
![alt text][image2]

---

### Clustering for segmentation implemented.

#### step1:   Create Cluster-Mask Point Cloud and Assign a color corresponding to each  segmented object
Just as the code between the lines 116-133.

#### step2:   Convert PCL data to ROS messages and Publish it
Just as the code below:  
ros_cluster_cloud = pcl_to_ros(cluster_cloud)  
pcl_clusters_pub.publish(ros_cluster_cloud)

After that we can get point cloud clustered objects, as the picture showed below:
![alt text][image3]

---
### Object recognition implemented.

#### step1:   Extract Features
To get better Features data for the SVM to train, i use HSV color channel to compute color histograms. The related code are in captrue_features.py and features.py; Also i modified the for loop in capture_features.py which makes each object is spawned 7 times randomly.

#### step2:   Train SVM
Use the output features file training_set_x.sav to feed the SVM then you can get the model_x.sav; The main code are in train_svm.py

#### step3:   Classify the objects and output the file output_x.yaml 
The code lies in project_template.py betweens 145-259.
* For the test1.world environment, my classifier identify 3/3 objects. As the 
pictures showed below:
![alt text][image7]
![alt text][image4]
  
---
* For the test2.world environment, my classifier identify 5/5 objects. As the 
pictures showed below:
![alt text][image8]
![alt text][image5]
  
---
* For the test3.world environment, my classifier identify 7/8 objects. As the 
pictures showed below:
![alt text][image9]
![alt text][image6]

---
### Improvement.
To better classify the objects, i think i should get more features, maybe 20 training set or more is better.
