# ML-and-DeepLearning-Projects-for-Beginners


# 1.  AI-Virtual-Painter-and-Mouse-Control-using-Computer-Vision-and-Hand-Tracking

  Open INSTALLATION GUIDE.txt to see how to run the program.
  
  Made this project using mediapipe for hand tracking, OpenCV for computer vision, and autopy for the mouse control. Works quite accurately and mouse movement can be smoothened or made faster by changing the 'smoothen' variable.
  If Index and Middle fingers are being detected as closed then either move closer to webcam or decrease the length condition in line 56 of 'AIVirtualPainter.py'.
  
  Mouse Control:
  
  1. Hold Index finger up to move mouse around the screen (both hands can be used but not simultaneously).
  2. hold Both the Index and Middle finger up but spread both fingers away from each other.
  3. Quickly close both fingers to make a click and then spread them away again.
  4. Hold only Index finger up again to move mouse and repeat.
  5. Press q on your keboard to stop the program.

  PAINTER:

  1. Run program.
  2. Hold both Index and Middle finger up for tool selection
  3. Go to the tool area on the webcam feed to select the item.
  4. Hold only Index finger up to start painting.
  5. Hold both Index and Middle finger up to select different tool.
  6. Repeat
  7. Press q on your keyboard to save the Canvas as image

  Find it [here](https://github.com/sarmadahmad8/ML-and-DeepLearning-Projects-for-Beginners/tree/main/AI%20Virtual%20Painter%20and%20Mouse%20using%20Computer%20Vision%20and%20Hand%20Tracking).

# 2. Amazon-Reviews-Sentiment-Analysis-using-NLP-and-DeepLearning

  Alot of projects using this dataset have been already done, however i did not find any particular project that used transformers to do sentiment analysis.
  I decided to make one of my own and surprisingly got better accuracy than all of the projects I came across.
  I started with a test model using fastAI as you can develop a model in a few lines of code however that did not bring about great results. 
  Decided to give it another try using Huggingface Transformers library and achieved an accuracy of 94%.
  Im pretty sure using ensemble techniques or TTA will give even better results and I aim to test that out when I have the time later.

  Find it [here](https://github.com/sarmadahmad8/ML-and-DeepLearning-Projects-for-Beginners/tree/main/Amazon%20Reviews%20Sentiment%20Analysis%20using%20NLP%20and%20DeepLearning).

# 3.  CAPTCHA-Text-Recognition-using-CRNN-Pytorch
  CAPTCHA Text Recognition using CRNN in Pytorch.
  Built from scratch using mostly pytorch.
  Custom architecture and text encoding and decoding technique.
  90% accuracy on test set.

  Find it [here](https://github.com/sarmadahmad8/ML-and-DeepLearning-Projects-for-Beginners/tree/main/CAPTCHA-Text-Recognition-using-CRNN-Pytorch).

# 4. Pets-Classifier-46-classes

  Built a Pets classifier which takes an image as an input and predicts the breed of dog/cat with 93% accuracy.
  Built using the Oxford-IIIT dataset of 37 different pet classes.
  
  Added a few more categories of dogs and cats that can be seen in the subcontinent namely:  'German_Shephard','Golden_Retriever','Labrador','Siberian_Husky','Alaskan_Malamute','American_Bobtale','Cyprus_Cat','Europian_Shorthair','Korat_Cat'.
  
  Deployed the model on huggingface spaces using Gradio and Git.
  
  The application can be visited and tested here: https://huggingface.co/spaces/sarmadahmad8/Pets_Classifier

  Find it [here](https://github.com/sarmadahmad8/ML-and-DeepLearning-Projects-for-Beginners/tree/main/PETS-Classifier-using-DeepLearning).

# 5.Book Recommender System using Classical Machine Learning Techniques

  In this project, I have developed a book recommender system using a combination of five different techniques to enhance recommendation accuracy and provide diverse recommendation strategies. The techniques used are:
  Techniques Used
  1. Decision Trees (DT)
  2. K-Nearest Neighbors (KNN)
  3. Random Forest (RF)
  4. LightGBM
  5. Collaborative Filtering
  
  Find it [here](https://github.com/sarmadahmad8/ML-and-DeepLearning-Projects-for-Beginners/tree/main/Book-Recommender-System-using-classical-ML-techniques).
