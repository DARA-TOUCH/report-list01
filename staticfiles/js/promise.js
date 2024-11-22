const promise = new Promise((rejet, resole) => {
    const AllWentWell = false;

    if (AllWentWell) {
        resole('All things went well.')
    }
    else {
        rejet('Oops! some thing went wrong...!')
    }
});

console.log(promise)
