function updateCart(productId, action) {
    console.log('Updating cart...');

    var url = '/update_cart/';
    var data = {
        product_id: productId,
        action: action,
        csrfmiddlewaretoken: csrftoken
    };

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            console.log('Cart updated successfully:', data);

            // Ensure quantity is not less than 0
            var quantity = Math.max(data.quantity, 0);

            // Update the cart data in the 'cart' object with the clamped quantity
            cart[productId] = quantity;

            // Update the quantity for the specific item on the page
            updateCartItemQuantity(productId, quantity);
        })
        .catch(error => console.error('Error updating cart:', error));
}


function getCartFromSession() {
    var url = '/get_cart/';
    fetch(url)
        .then(response => response.json())
        .then(data => {
            cart = data;
            console.log('CART:', cart);
            updateCartItemQuantity();
        })
        .catch(error => console.error('Error retrieving cart:', error));
}

// Get the initial cart data from the server when the page loads
getCartFromSession();

var updateBtns = document.getElementsByClassName('update-cart');

for (i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        var productId = this.dataset.product;
        var action = this.dataset.action;
        console.log('productId:', productId, 'Action:', action);

        updateCart(productId, action);
    });
}

function updateCartItemQuantity(productId, quantity) {
    // Update the quantity for the specific item on the page
    var quantityElement = document.getElementById('quantity-' + productId);
    console.log('quantity:', quantity)
    if (quantityElement) {
        quantityElement.textContent = quantity;

    }

}

document.addEventListener('click', function (event) {
    if (event.target.classList.contains('delete-item')) {
        event.preventDefault();
        var productId = event.target.dataset.product;
        deleteCartItem(productId);
    }
});

function deleteCartItem(productId) {
    console.log('Deleting item from cart...');

    var url = '/delete_cart_item/';
    var data = {
        product_id: productId,
        csrfmiddlewaretoken: csrftoken
    };

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            console.log('Item removed successfully:', data);

            // Update the cart data in the 'cart' object
            delete cart[productId];

            // Update the quantity for the specific item on the page
            updateCartItemQuantity(productId, 0);
            location.reload();

        })
        .catch(error => console.error('Error deleting item from cart:', error));

}