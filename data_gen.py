from tensorflow.keras.preprocessing.image import ImageDataGenerator

TRAIN_DIR = 'content/spectrograms/train'
TEST_DIR = 'content/spectrograms/test'

def create_generators(batch_size=64):
    batch_size = batch_size
    img_size = (288, 432)

    # flow_from_directory automatically infers the labels using our directory structure and encodes them accordingly.
    train_datagen = ImageDataGenerator(rescale=1./255)
    train_generator = train_datagen.flow_from_directory(TRAIN_DIR,target_size=img_size,color_mode='rgba',class_mode='categorical',batch_size=batch_size, shuffle=True)
    
    vali_datagen = ImageDataGenerator(rescale=1./255)
    vali_generator = vali_datagen.flow_from_directory(TEST_DIR,target_size=img_size,color_mode='rgba',class_mode='categorical',batch_size=batch_size, shuffle=True) 

    return (train_generator, vali_generator)
    
def main():
    train, vali = create_generators()
    print(next(vali)[0].shape)

if __name__ == '__main__':
    main()

