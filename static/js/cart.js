/*=========================================
    BETHAK CAFE - CART UTILITY (shared)
    Used by: menu.html, viewcart.html
    Storage: localStorage key "bethak_cart"
=========================================*/

(function () {
    "use strict";

    var CART_KEY = "bethak_cart";

    function getCart() {
        try {
            return JSON.parse(localStorage.getItem(CART_KEY)) || [];
        } catch (e) {
            return [];
        }
    }

    function saveCart(cart) {
        localStorage.setItem(CART_KEY, JSON.stringify(cart));
        updateCartBadge();
    }

    function addToCart(item) {
        var cart = getCart();
        var existing = null;
        for (var i = 0; i < cart.length; i++) {
            if (cart[i].name === item.name) { existing = cart[i]; break; }
        }
        if (existing) {
            existing.qty += 1;
        } else {
            cart.push({ name: item.name, price: Number(item.price), qty: 1 });
        }
        saveCart(cart);
        showCartToast(item.name + " added to cart");
    }

    function removeFromCart(name) {
        var cart = getCart().filter(function (i) { return i.name !== name; });
        saveCart(cart);
    }

    function updateQty(name, qty) {
        var cart = getCart();
        qty = parseInt(qty, 10);
        for (var i = 0; i < cart.length; i++) {
            if (cart[i].name === name) {
                if (isNaN(qty) || qty <= 0) {
                    cart.splice(i, 1);
                } else {
                    cart[i].qty = qty;
                }
                break;
            }
        }
        saveCart(cart);
    }

    function clearCart() {
        saveCart([]);
    }

    function getCartCount() {
        return getCart().reduce(function (sum, i) { return sum + i.qty; }, 0);
    }

    function getCartTotal() {
        return getCart().reduce(function (sum, i) { return sum + (i.qty * i.price); }, 0);
    }

    function updateCartBadge() {
        var count = getCartCount();
        var badges = document.querySelectorAll(".cart-count");
        for (var i = 0; i < badges.length; i++) {
            badges[i].textContent = count;
        }
    }

    function showCartToast(message) {
        var toast = document.getElementById("cartToast");
        if (!toast) {
            toast = document.createElement("div");
            toast.id = "cartToast";
            toast.className = "cart-toast";
            document.body.appendChild(toast);
        }
        toast.textContent = message;
        toast.classList.add("show");
        clearTimeout(window.__cartToastTimer);
        window.__cartToastTimer = setTimeout(function () {
            toast.classList.remove("show");
        }, 1800);
    }

    /* Generates a simple unique booking / order ID */
    function generateOrderId() {
        var stamp = Date.now().toString().slice(-6);
        return "ORD" + stamp;
    }

    window.BethakCart = {
        getCart: getCart,
        saveCart: saveCart,
        addToCart: addToCart,
        removeFromCart: removeFromCart,
        updateQty: updateQty,
        clearCart: clearCart,
        getCartCount: getCartCount,
        getCartTotal: getCartTotal,
        generateOrderId: generateOrderId
    };

    document.addEventListener("DOMContentLoaded", updateCartBadge);
})();

