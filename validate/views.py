from django.shortcuts import render,redirect
import sys
from django.http import HttpResponseRedirect
from PIL import Image
from .forms import HotelForm as hform
from .models import validate as output
from pathlib import Path
import os
import cv2
import tensorflow as tf
from object_detection.utils import label_map_util
import numpy as np
sys.path.append("..")

from object_detection.utils import visualization_utils as vis_util

MODEL_NAME = 'inference_graph'

# Grab path to current working directory
CWD_PATH = os.getcwd()

# Path to frozen detection graph .pb file, which contains the model that is used
# for object detection.
PATH_TO_CKPT = os.path.join(CWD_PATH, MODEL_NAME, 'frozen_inference_graph.pb')

# Path to label map file
PATH_TO_LABELS = os.path.join(CWD_PATH, 'training', 'labelmap.pbtxt')
NUM_CLASSES = 3
# Number of classes the object detector can identify
img_detect = ""
def image_request(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = hform(request.POST, request.FILES)
            BASE_DIR = Path(__file__).absolute().parent.parent
            Save_DIR = os.path.join(BASE_DIR, "media\images")
            img_url = request.FILES['image']
            img_in = os.path.join(Save_DIR,str(img_url))
            print(img_in)
            nam = request.POST.get('name ')
            if form.is_valid():
                form.save()
                img_obj = form.instance
                img_url = img_obj.image.url
                nam = img_obj.name
                #out_img = str(BASE_DIR) + img_url
                # print(out_img)



                ## Load the label map.
                # Label maps map indices to category names, so that when our convolution
                # network predicts `5`, we know that this corresponds to `king`.
                # Here we use internal utility functions, but anything that returns a
                # dictionary mapping integers to appropriate string labels would be fine
                label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
                categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                                            use_display_name=True)
                category_index = label_map_util.create_category_index(categories)

                # Load the Tensorflow model into memory.
                detection_graph = tf.Graph()
                with detection_graph.as_default():
                    od_graph_def = tf.compat.v1.GraphDef()
                    with tf.io.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
                        serialized_graph = fid.read()
                        od_graph_def.ParseFromString(serialized_graph)
                        tf.import_graph_def(od_graph_def, name='')

                    sess = tf.compat.v1.Session(graph=detection_graph)

                # Define input and output tensors (i.e. data) for the object detection classifier

                # Input tensor is the image
                image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

                # Output tensors are the detection boxes, scores, and classes
                # Each box represents a part of the image where a particular object was detected
                detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

                # Each score represents level of confidence for each of the objects.
                # The score is shown on the result image, together with the class label.
                detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
                detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

                # Number of objects detected
                num_detections = detection_graph.get_tensor_by_name('num_detections:0')

                #img = cv2.imread('F:\Project\Django\\nrpu\\validate\sample.jpg')

                img = cv2.imread(img_in)
                # print(out_img)

                i = 0

                while (True):

                    # Acquire frame and expand frame dimensions to have shape: [1, None, None, 3]
                    # i.e. a single-column array, where each item in the column has the pixel RGB value
                    # ret, frame = video.read()
                    frame = img
                    frame_expanded = np.expand_dims(frame, axis=0)

                    # Perform the actual detection by running the model with the image as input
                    (boxes, scores, classes, num) = sess.run(
                        [detection_boxes, detection_scores, detection_classes, num_detections],
                        feed_dict={image_tensor: frame_expanded})

                    # Draw the results of the detection (aka 'visulaize the results')
                    vis_util.visualize_boxes_and_labels_on_image_array(
                        frame,
                        np.squeeze(boxes),
                        np.squeeze(classes).astype(np.int32),
                        np.squeeze(scores),
                        category_index,
                        use_normalized_coordinates=True,
                        line_thickness=8,
                        min_score_thresh=0.51)


                    if i == 10:
                        i = 0
                        im = Image.fromarray(frame)
                        img_detect = "\\media\\bacteria_detect\\" + nam + ".jpg"
                        img_detect1 = str(BASE_DIR) + img_detect
                        im.save(img_detect1)
                        print(classes)
                        break

                    i += 1
                classes = np.unique(classes)
                print(classes)
                classes = classes.tolist()
                bacteria = []
                for category in classes:
                    if category == 1:
                        bacteria.append("E Coli")
                    elif category == 3:
                        bacteria.append("Yeast")

                request.session['img_detect'] = img_detect
                request.session['classes'] = bacteria


                return render(request, 'validate/test_sample.html', {'form': form, 'img_obj': img_obj, 'img_detect': img_detect})
        else:
            form = hform()
        return render(request, 'validate/test_sample.html', {'form': form})
    else:
        return redirect('authentication:login_user')


def reporting(request):
    # SAVE_DIR = image_request(request)
    img_detect = request.session['img_detect']
    classes = request.session['classes']
    form = output.objects.all().last()
    print(img_detect)
    return render(request,'validate/reporting.html',{'form':form, 'image_detect':img_detect, 'classes' : classes})