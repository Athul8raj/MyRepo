#from tensorflow.keras.models import Sequential
#from tensorflow.keras.layers import Dense,Dropout,Activation,BatchNormalization
import pandas as pd
import tensorflow as tf

X_train = pd.read_csv('train\X_train.txt',delim_whitespace=True,na_filter=False,header=None)
X_train.fillna(-99999,inplace=True)
y_train = pd.read_csv('train\y_train.txt',names=['Label'])
y_train = [int(i)-1 for i in list(y_train['Label'])]
X_test = pd.read_csv('test\X_test.txt',delim_whitespace=True,na_filter=False,header=None)
y_test = pd.read_csv('test\y_test.txt',names=['Label'])
y_test = [int(i)-1 for i in list(y_test['Label'])]

#model = Sequential()
#model.add(Dense(40,input_shape=X_train.shape[1:]))
#model.add(Activation('relu'))
#model.add(Dropout(0.4))
#model.add(BatchNormalization())
#
#model.add(Dense(6))
#model.add(Activation('softmax'))
#
#model.compile(loss='sparse_categorical_crossentropy',optimizer='adam',metrics=['accuracy'])
#
#model.fit(X_train,y_train,epochs=10,validation_split=0.05)
#model.save('HAR.model')

model = tf.keras.models.load_model('HAR.model')

Y_pred = model.predict([X_test])
y_classes = Y_pred.argmax(axis=-1)

total =0
count=0
for i in y_classes:
    total +=1
    if i in y_test:
        count+=1
        
print(count/total)