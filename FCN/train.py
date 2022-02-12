import os
import tensorflow as tf
from model import FCN_model, FCN_Dense_model
from generator import Generator

def train(model, train_generator, test_generator, directory_path, modeltype, epochs = 30):
    """
    This is the function that will be called for training the model.
    It can be used for both the FCN_model and the FCN_model.
    The train_generator and test generator need to be created by creating generator objects, using the testing and training
    datasets.
    """
    #compiling the model
    model.compile(optimizer=tf.keras.optimizers.Adam(lr=0.001), loss='categorical_crossentropy', metrics=['accuracy'])
    #creating directory for the models, but only if it does not already exist
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    #creating a file name that gives information about the model
    model_path = os.path.join(directory_path, f'(Model:{modeltype})_(Epoch:{epoch:02d})_(Loss:{loss:.2f})_(Accuracy:{acc:.2f}).h5')
    #training the model
    #model.fit returns a history callback object which contains the accuracy, loss, and other training metrics for each epoch
    model_history = model.fit(
        generator = train_generator,
        steps_per_epoch = len(train_generator),
        epochs = epochs,
        callbacks = [tf.keras.callbacks.ModelCheckpoint(model_path, monitor='val_loss', save_best_only=True, verbose=1)],
        validation_data = test_generator,
        validation_steps = len(test_generator)
    )
    #returning information about the model
    return model_history