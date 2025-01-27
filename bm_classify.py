import numpy as np

#######################################################
# DO NOT MODIFY ANY CODE OTHER THAN THOSE TODO BLOCKS #
#######################################################

def binary_train(X, y, loss="perceptron", w0=None, b0=None, step_size=0.5, max_iterations=1000):
    """
    Inputs:
    - X: training features, a N-by-D numpy array, where N is the
    number of training points and D is the dimensionality of features
    - y: binary training labels, a N dimensional numpy array where
    N is the number of training points, indicating the labels of
    training data (either 0 or 1)
    - loss: loss type, either perceptron or logistic
	- w0: initial weight vector (a numpy array)
	- b0: initial bias term (a scalar)
    - step_size: step size (learning rate)
    - max_iterations: number of iterations to perform gradient descent
    Returns:
    - w: D-dimensional vector, a numpy array which is the final trained weight vector
    - b: scalar, the final trained bias term
    Find the optimal parameters w and b for inputs X and y.
    Use the *average* of the gradients for all training examples
    multiplied by the step_size to update parameters.
    """
    N, D = X.shape
    assert len(np.unique(y)) == 2

    w = np.zeros(D)
    if w0 is not None:
        w = w0

    b = 0
    if b0 is not None:
        b = b0

    if loss == "perceptron":

        for i in range(max_iterations):
            val = X@w + b
            fake = np.where(y == 1, 1, -1)
            mask = np.where((val * fake) <= 0, -1, 0) * fake
            grad_w = np.sum(mask.reshape(-1, 1)*X, axis=0)
            grad_b = np.sum(mask, axis=0)
            w -= (step_size/N) * grad_w
            b -= (step_size/N) * grad_b




    elif loss == "logistic":

        for i in range(max_iterations):
            val = X@w + b
            fake = np.where(y == 1, 1, -1)
            z = val * fake
            grad = -np.exp(-z) / (1 + np.exp(-z)) * fake
            grad_w = np.sum(grad.reshape(-1, 1) * X, axis=0)
            grad_b = np.sum(grad, axis=0)
            w -= (step_size/N) * grad_w
            b -= (step_size/N) * grad_b



    else:
        raise "Undefined loss function."

    assert w.shape == (D,)
    return w, b

def sigmoid(z):

    """
    Inputs:
    - z: a numpy array or a float number
    
    Returns:
    - value: a numpy array or a float number after applying the sigmoid function 1/(1+exp(-z)).
    """

    ############################################
    # TODO 3 : fill in the sigmoid function    #
    ############################################

    return 1/(1 + np.exp(-z))


def binary_predict(X, w, b):
    """
    Inputs:
    - X: testing features, a N-by-D numpy array, where N is the
    number of training points and D is the dimensionality of features
    - w: D-dimensional vector, a numpy array which is the weight
    vector of your learned model
    - b: scalar, which is the bias of your model

    Returns:
    - preds: N-dimensional vector of binary predictions (either 0 or 1)
    """
    N, D = X.shape

    #############################################################
    # TODO 4 : predict DETERMINISTICALLY (i.e. do not randomize)#
    #############################################################
    val = X @ w + b
    preds = np.where(val>0, 1, 0)

    assert preds.shape == (N,)
    return preds

def multiclass_train(X, y, C,
                     w0=None,
                     b0=None,
                     gd_type="sgd",
                     step_size=0.5,
                     max_iterations=1000):
    """
    Inputs:
    - X: training features, a N-by-D numpy array, where N is the
    number of training points and D is the dimensionality of features
    - y: multiclass training labels, a N dimensional numpy array where
    N is the number of training points, indicating the labels of
    training data (0, 1, ..., C-1)
    - C: number of classes in the data
    - gd_type: gradient descent type, either GD or SGD
    - step_size: step size (learning rate)
    - max_iterations: number of iterations to perform (stochastic) gradient descent

    Returns:
    - w: C-by-D weight matrix, where C is the number of classes and D
    is the dimensionality of features.
    - b: a bias vector of length C, where C is the number of classes

    Implement multinomial logistic regression for multiclass
    classification. Again for GD use the *average* of the gradients for all training
    examples multiplied by the step_size to update parameters.

    You may find it useful to use a special (one-hot) representation of the labels,
    where each label y_i is represented as a row of zeros with a single 1 in
    the column that corresponds to the class y_i. Also recall the tip on the
    implementation of the softmax function to avoid numerical issues.
    """

    N, D = X.shape

    w = np.zeros((C, D))
    if w0 is not None:
        w = w0

    b = np.zeros(C)
    if b0 is not None:
        b = b0

    np.random.seed(42) #DO NOT CHANGE THE RANDOM SEED IN YOUR FINAL SUBMISSION
    if gd_type == "sgd":

        for it in range(max_iterations):
            n = np.random.choice(N)
            x = X[n]
            one_hot_y = np.eye(C)[y[n]]
            val = np.dot(w, x.T) + b
            nor = np.exp(val - np.max(val))
            grad_b = (nor/np.sum(nor)) - one_hot_y
            grad_w = grad_b.reshape(-1,1) @ x.reshape(1,-1)
            w -= (step_size)*grad_w
            b -= (step_size)*grad_b



    elif gd_type == "gd":
        for iter in range(max_iterations):
            one_hot_y = (np.eye(C)[y]).T
            val = np.dot(w, X.T) + b.reshape(-1, 1)
            nor = np.exp(val - np.max(val, axis=0))
            a = (nor / np.sum(nor, axis=0)) - one_hot_y
            grad_w = np.dot(a, X)
            grad_b = np.sum(a, axis=1)

            w -= (step_size/N)*grad_w
            b -= (step_size/N)*grad_b

    else:
        raise "Undefined algorithm."


    assert w.shape == (C, D)
    assert b.shape == (C,)

    return w, b


def multiclass_predict(X, w, b):
    """
    Inputs:
    - X: testing features, a N-by-D numpy array, where N is the
    number of training points and D is the dimensionality of features
    - w: weights of the trained model, C-by-D
    - b: bias terms of the trained model, length of C

    Returns:
    - preds: N dimensional vector of multiclass predictions.
    Predictions should be from {0, 1, ..., C - 1}, where
    C is the number of classes
    """
    N, D = X.shape

    val = np.dot(w, X.T) + b.reshape(-1,1)
    nor = np.exp(val - np.max(val, axis=0))
    preds = np.argmax(nor/np.sum(nor,axis=0),axis=0)
    assert preds.shape == (N,)
    return preds