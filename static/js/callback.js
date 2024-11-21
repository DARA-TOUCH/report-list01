const showMessage = (callback) => {
    console.log(callback);
};

const firstMessage = (callback) => {
    setTimeout(() => {
        showMessage('Hello');
        callback();
    }, 2000);
};

const secondMessage = () => {
    showMessage('world...!');
};

function Test() {
    let x = 3;
    const y = 50;
    console.log(x + y)
    return x + y
}

firstMessage(secondMessage);
firstMessage(Test);