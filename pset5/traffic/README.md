# Experimentation Process

In order to tackle the task at hand, I followed a systematic process of experimentation to find the most effective configuration for the model. Here's a summary of my attempts and their outcomes:

### 1st Attempt
For the initial attempt, I copied the code from `handwriting.py` and made only minor changes to the input and output shapes to fit the current problem. Unfortunately, this configuration resulted in poor performance, with an accuracy of only 0.0550.

### 2nd Attempt
In the second attempt, I changed the loss function to `binary_crossentropy`, hoping for a slight improvement. Although the accuracy increased marginally to 0.0568, it remained unsatisfactory.

### 3rd Attempt
For the third attempt, I made significant modifications to the model architecture. I increased the number of filters in the initial `Conv2D` layer to 64, changed the pooling size to `(4, 4)`, and increased the number of units in the dense hidden layer to 512. This adjustment resulted in a remarkable improvement in accuracy, reaching 94.5%. However, the training time noticeably increased.

### 4th Attempt
In the fourth attempt, I experimented with a more complex model architecture, including additional layers and dropout regularization. However, this configuration proved to be ineffective. It required an extensive amount of time to train, and the accuracy only improved by 1%.

### 5th Attempt
Based on the successful third attempt, I made a minor adjustment by increasing the filters in the initial `Conv2D` layer to 128. This change resulted in a 1% increase in accuracy, while maintaining a reasonable training time.

### 6th Attempt
In the sixth attempt, I decided to modify the max pooling size to `(2, 2)`, while keeping the `Conv2D` layer at 64 filters. Although the accuracy improved to 95%, the training time was not optimal.

### 7th Attempt
To further explore the impact of the dense hidden layer, I doubled the number of units to 1024, while maintaining the 64 filters in the `Conv2D` layer and a max pooling size of `(4, 4)`. Unfortunately, this adjustment resulted in a decrease of approximately 2% in accuracy.

### 8th Attempt
In an attempt to optimize the training time, I reduced the number of units in the dense hidden layer to 256, while keeping the other parameters the same as in the seventh attempt. Although the training time significantly improved, the accuracy dropped by approximately 4%.

### 9th Attempt
Returning to the successful third attempt, I decided to further enhance the model architecture. I added an additional `Conv2D` layer with 128 filters and modified the pooling size to `(2, 2)` before the existing `Conv2D` layer with 64 filters. This configuration yielded outstanding results, achieving an accuracy of 98% with reasonable training time.

### 10th Attempt
Building upon the ninth attempt, I introduced another `Conv2D` layer with 32 filters and a max pooling layer before the existing `Conv2D` layer with 64 filters. Although this adjustment reduced the training time by half, it also resulted in a decrease in accuracy to 96%.

## Conclusion
Overall, the experimentation process involved iteratively modifying the model architecture and observing the impact on accuracy and training time. The most successful configuration consisted of two `Conv2D` layers (64 and 128 filters), max pooling layers, a dense hidden layer with 512 units, and a dropout layer. This configuration achieved an impressive accuracy of 98% while maintaining reasonable training time.
&nbsp;

##### Acknowledgement:
I would like to acknowledge that while the experiments and observations presented in this documentation are my own, I sought assistance from ChatGPT to help me refine the phrasing and structure of this README. The aim was to ensure that the final document adheres to the standards expected for a well-documented project. However, I want to emphasize that the content, including the code and observations, remains entirely my work. I believe in upholding the code of honor and integrity, which is why I have disclosed the use of AI assistance in the writing process.