from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf
import numpy as np
import pymysql
import model


def train(model, data, sess, training_iters=100000, display_step=5000):
    train_writer = tf.summary.FileWriter('./train', sess.graph)
    sess.run(init)
    step = 1
    while step <= training_iters:
        batch_xs, batch_ys = data.next_batch()
        # batch_xs = batch_xs.reshape((model.batch_size, model.steps, model.inputs))
        sess.run(model.optimizer, feed_dict={model.x: batch_xs, model.y: batch_ys, model.keep_prob: 0.5})
        if step % display_step == 0:
            summary, loss, acc = sess.run([model.merged, model.cost, model.accuracy], feed_dict={model.x: batch_xs, model.y: batch_ys, model.keep_prob: 1.0})
            train_writer.add_summary(summary, step)
            print("Iter " + str(step) + ", Minibatch Loss= " + "{:.6f}".format(loss) + ", Training Accuracy= " + "{:.5f}".format(acc))
        step += 1
    print("Optimization Finished!")


def test(model, data, sess):
    test_data, test_label = data.test_batch()
    test_data = test_data.reshape((-1, model.steps, model.inputs))
    test = sess.run(model.output, feed_dict={model.x: test_data, model.y: test_label, model.keep_prob:1.0})
    for i in range(model.batch_size):
        print test[i], test_label[i]

def save(sess):
    saver = tf.train.Saver()
    save_path = saver.save(sess, "./model/model.ckpt")
    print("Model saved in file: %s" % save_path)


if __name__ == "__main__":
    # mnist = input_data.read_data_sets("MNIST_data", one_hot=True)
    data = model.data(stock_name="AAPL")
    my_network = model.LSTM_layer(name="trading")
    init = tf.global_variables_initializer()
    with tf.Session() as sess:
        train(my_network, data, sess)
        test(my_network, data, sess)
        save(sess)