function build_cart(data){

}

window.addEventListener('DOMContentLoaded', function (e) {
    const cart = getCookie('cart');
    if (cart) {
        const data = {};
        for (let item of cart.split(',')) {
            const [pk, qty] = item.split(':');
            data[pk] = qty;
        }
        fetch("/orders/ajax/", {
            method: "POST",
            credentials: "same-origin",
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": getCookie("csrftoken"),
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
            .then(response => response.json())
            .then(data => {
                console.log(data)
                build_cart(data);
            });
    } else {
        showMessage('سبد خرید شما خالی است.', 'warning');
    }

})