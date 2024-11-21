function task1 (callback) {
    setTimeout(() => {
        console.log("1. Operation one...")
        callback();
    }, 1000)
};

function task2 (callback) {
    setTimeout(() => {
        console.log("2. Operation two...")    
        callback();
}, 1000);
};


task1(() => {
    task2(() => {
    })
})