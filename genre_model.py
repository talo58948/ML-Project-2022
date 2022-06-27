from tensorflow.keras.layers import Dense, Dropout,Flatten, Conv2D
from tensorflow.keras.layers import BatchNormalization, Activation, MaxPooling2D
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam

def genre_model(input_shape = (288,432,4),classes=7):
    model = Sequential()

    # 1st Conv
    model.add(Conv2D(8, kernel_size=(3,3), strides=(1,1), input_shape=input_shape)) # num_of_filters, kernel_size (size of each filter), strides (the steps that the 2d 'window' takes each time)
    model.add(BatchNormalization(axis=3)) # normalizes the output of the conv2D layer (makes every 'feature' on the same scale to avoid unexpected beahvior in the NN). let n = noramlized output. n = (n*g)+b. g,b are trainable, along with the mean and s.d of the inputs. this means that between batches, we optimize the batch normalization aswell. 
    model.add(Activation('relu')) # relu is a simple activation function that disrigards of negative inputs, setting them as 0. relu = (x) => {if x<0{return 0;} else {return x;}}
    model.add(MaxPooling2D((2,2))) # maxpooling2d goes through every image in the batch and reduces their resolution, by taking the max value of a sliding 2d window (with size of (2,2) in this case). it helps reducing the time of training and prevents overfitting by disregarding of the less meaningfull parts of the inputs.

    # 2nd Conv
    model.add(Conv2D(16, kernel_size=(3,3), strides=(1,1))) 
    model.add(BatchNormalization(axis=3)) 
    model.add(Activation('relu')) 
    model.add(MaxPooling2D((2,2)))

    # 3rd Conv
    model.add(Conv2D(32, kernel_size=(3,3), strides=(1,1))) 
    model.add(BatchNormalization(axis=3)) 
    model.add(Activation('relu')) 
    model.add(MaxPooling2D((2,2))) 

    # 4th Conv
    model.add(Conv2D(64, kernel_size=(3,3), strides=(1,1))) 
    model.add(BatchNormalization(axis=3)) 
    model.add(Activation('relu')) 
    model.add(MaxPooling2D((2,2))) 

    # 5th Conv
    model.add(Conv2D(128, kernel_size=(3,3), strides=(1,1))) 
    model.add(BatchNormalization(axis=3)) 
    model.add(Activation('relu')) 
    model.add(MaxPooling2D((2,2))) 

    # 6th Conv
    model.add(Conv2D(128, kernel_size=(3,3), strides=(1,1))) 
    model.add(BatchNormalization(axis=3)) 
    model.add(Activation('relu')) 
    model.add(MaxPooling2D((2,2))) 

    model.add(Flatten())
    # flattens the 4d tensor of inputs 
    # a spectrogram is an image who is represented as a 3d tensor, a batch of spectrograms is obviously a 4d tensor (batch_size, width (288 here), height (288 here), color_channel (normally 4))
    model.add(Dropout(rate=0.3)) # to avoid overfitting https://www.google.com/url?sa=i&url=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FOverfitting&psig=AOvVaw2t6bcb7vFAzb7L6zyQcVDY&ust=1647293545837000&source=images&cd=vfe&ved=0CAsQjRxqFwoTCKia_uaExPYCFQAAAAAdAAAAABAD
    
    model.add(Dense(256, activation='relu'))
    model.add(BatchNormalization())
    model.add(Dropout(rate=0.3))

    model.add(Dense(classes, activation='softmax')) # a fully connected layer to the 9 outputs of the NN.

    opt = Adam(learning_rate=5e-5)
    model.compile(optimizer=opt, loss='categorical_crossentropy',metrics=['accuracy'])
    model.summary()
    return model

if __name__ == '__main__':
    model = genre_model()