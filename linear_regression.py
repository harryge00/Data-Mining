import tensorflow as tf

# Model parameters
theta1 = tf.Variable([1.1], dtype=tf.float32)
theta2 = tf.Variable([-8], dtype=tf.float32)
theta0 = tf.Variable([-159], dtype=tf.float32)
# Model input and output
living_area = tf.placeholder(tf.float32)
bedrooms = tf.placeholder(tf.float32)
linear_model = theta1 * living_area + theta2 * bedrooms + theta0
price = tf.placeholder(tf.float32)


# loss
loss = tf.reduce_sum(tf.square(linear_model - price)) # sum of the squares
# optimizer
optimizer = tf.train.GradientDescentOptimizer(10)
train = optimizer.minimize(loss)

# training data
living_area_train = [2104, 1600, 2400, 1416, 3000]
bedrooms_train = [3, 3, 3, 2, 4]
price_train = [400, 330, 369, 232, 540]

# training loop
init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init) # reset values to wrong
print(sess.run(linear_model, {living_area: living_area_train,  bedrooms: bedrooms_train}))
print(living_area_train)
for i in range(4000):
  sess.run(train, {living_area: living_area_train,  bedrooms: bedrooms_train, price: price_train})

print(theta1, theta2, theta0)

# evaluate training accuracy
curr_t1, curr_t2, curr_t0, curr_loss = sess.run([theta1, theta2, theta0, loss], {living_area: living_area_train,  bedrooms: bedrooms_train, price: price_train})
print("t1: %s t2: %s t0: %s  loss: %s"%(curr_t1, curr_t2, curr_t0, curr_loss))