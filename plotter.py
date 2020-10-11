import matplotlib.pyplot as plt
import pickle

def plot_learning_curves(history, pos, name):
    acc = history['accuracy']
    val_acc = history['val_accuracy']
    
    loss = history['loss']
    val_loss = history['val_loss']
    
    plt.subplot(2, 4, pos)
    plt.plot(acc, label='Training Accuracy')
    plt.plot(val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.ylabel('Accuracy')
    plt.ylim([0,1])
    plt.title(name+' Training and Validation Accuracy')
    
    plt.subplot(2, 4, pos+4)
    plt.plot(loss, label='Training Loss')
    plt.plot(val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.ylabel('Cross Entropy')
    plt.ylim([min(plt.ylim()),max(plt.ylim())])
    plt.title(name+' Training and Validation Loss')
    plt.xlabel('epoch')

hists = []
with open('hists.pkl', 'rb') as f:
    hists = pickle.load(f)
simple_hist,io_hist, adv_hist, vrigin_adv_hist = hists[0]

plot_learning_curves(simple_hist, 1, 'Simple')
plot_learning_curves(adv_hist, 2, 'Combined')
plot_learning_curves(vrigin_adv_hist, 3, 'Extended')
plot_learning_curves(io_hist, 4, 'Transformation')

plt.show()    