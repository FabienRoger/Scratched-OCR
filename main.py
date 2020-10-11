from datacreator import *
from network import *
from constants import *
import matplotlib.pyplot as plt
import numpy as np
import pickle

### Simple ###

train_gen,val_gen = DataCreator().simple_train_generators()
pred_gen = DataCreator().simple_predict_generator()
print("gen done")

simple_net = Network(name = 'Simple')
print("net created")
#net.load()

simple_hist = simple_net.train(train_gen,val_gen,20,verbose = 1)
print("net trained")
simple_net.save()

### Transformation ###

io_train_gen,io_val_gen = DataCreator().io_train_generators()
io_pred_gen = DataCreator().io_predict_generator()
print("gen done")

io_net = Network(net = 'io',ks=5, name = 'Transformation', learning_rate=0.0004)

print("io_net created")
#net.load()

io_hist = io_net.train(io_train_gen,io_val_gen,10,verbose = 1)
print("io_net trained")
io_net.save()

### Combined ###

net = Network(net='advanced', io_model=io_net.model, name = 'my predictor')
print("net created")
#net.load()

adv_hist = net.train(train_gen,val_gen,20,verbose = 1)
print("net trained")
net.save()

### Extended ###

virgin_io_net = Network(net = 'io',ks=5, name = 'Transformation with random weights', learning_rate=0.0004)
virgin_adv_net = Network(net='advanced', io_model=virgin_io_net.model, name = 'Extended')
vrigin_adv_hist = net.train(train_gen,val_gen,30,verbose = 1)

### Saving training history ###

hists = []
hists.append([h.history for h in [simple_hist,io_hist, adv_hist, vrigin_adv_hist]])

with open('hists.pkl', 'wb') as f:
    pickle.dump(hists,f)

### Printing an image cleaned by the Transformation network and the corresponding input scratched image ###

pred_gen2 = DataCreator().io_predict_generator()
pred = io_net.predict(io_pred_gen, verbose = 1)
plt.figure(figsize=(8, 8))
plt.subplot(2, 1, 1)
plt.imshow(next(pred_gen2)[0].reshape((IMG_SIZE, IMG_SIZE)), cmap='gray', vmin=0, vmax=1)
plt.subplot(2, 1, 2)
plt.imshow(pred[0].reshape((IMG_SIZE, IMG_SIZE)), cmap='gray', vmin=0, vmax=1)
plt.show()