/*=========================================
    BETHAK CAFE - ALL JS ANIMATIONS
    (self-contained: injects its own CSS,
    no changes needed in any .css file)
=========================================*/

(function () {
    "use strict";

    /* -----------------------------------------
        0) INJECT REQUIRED CSS (once)
    ----------------------------------------- */
    var style = document.createElement("style");
    style.textContent =
        ".reveal-el{opacity:0;transform:translateY(40px);transition:opacity .8s ease,transform .8s ease;}" +
        ".reveal-el.in-view{opacity:1;transform:translateY(0);}" +
        ".ripple{position:absolute;border-radius:50%;background:rgba(255,255,255,.6);transform:scale(0);animation:rippleEffect .6s linear;pointer-events:none;}" +
        "@keyframes rippleEffect{to{transform:scale(4);opacity:0;}}" +
        ".shake-error{animation:inputShakeJS .4s ease;}" +
        "@keyframes inputShakeJS{0%,100%{transform:translateX(0);}20%,60%{transform:translateX(-8px);}40%,80%{transform:translateX(8px);}}";
    document.head.appendChild(style);


    /* -----------------------------------------
        1) SCROLL REVEAL ANIMATION
        Cards/sections fade + slide up
        the first time they scroll into view.
    ----------------------------------------- */
    var revealSelectors = [
        ".chef-card", ".review-card", ".menu-card",
        ".contact-box", ".booking-content", ".map-box",
        ".gallery-top", ".gallery-bottom", ".service-icon",
        ".table-card"
    ].join(",");

    var revealEls = document.querySelectorAll(revealSelectors);

    if (revealEls.length && "IntersectionObserver" in window) {
        var revealObserver = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add("in-view");
                    revealObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.15 });

        revealEls.forEach(function (el) {
            el.classList.add("reveal-el");
            revealObserver.observe(el);
        });
    }


    /* -----------------------------------------
        2) BUTTON RIPPLE (click animation)
    ----------------------------------------- */
    var rippleSelectors = ".login-btn, .register-btn, .reserve-btn, .choose-table-btn";
    document.querySelectorAll(rippleSelectors).forEach(function (btn) {
        var computedPos = window.getComputedStyle(btn).position;
        if (computedPos === "static") btn.style.position = "relative";
        btn.style.overflow = "hidden";

        btn.addEventListener("click", function (e) {
            var rect = btn.getBoundingClientRect();
            var size = Math.max(rect.width, rect.height);
            var circle = document.createElement("span");
            circle.className = "ripple";
            circle.style.width = circle.style.height = size + "px";
            circle.style.left = (e.clientX - rect.left - size / 2) + "px";
            circle.style.top = (e.clientY - rect.top - size / 2) + "px";
            btn.appendChild(circle);
            setTimeout(function () { circle.remove(); }, 600);
        });
    });


    /* -----------------------------------------
        3) FORM SHAKE ON INVALID FIELD
        (login.html, register.html, reservation.html)
    ----------------------------------------- */
    document.querySelectorAll("form").forEach(function (form) {
        form.querySelectorAll("input[required], select[required], textarea[required]")
            .forEach(function (field) {
                field.addEventListener("invalid", function () {
                    var wrapper = field.closest(".input-box, .textarea-box") || field;
                    wrapper.classList.remove("shake-error");
                    void wrapper.offsetWidth; // restart animation
                    wrapper.classList.add("shake-error");
                });
            });
    });


    /* -----------------------------------------
        4) COUNTER-UP (numbers count up on scroll)
        Usage in HTML:
        <span data-counter="500">0</span>
    ----------------------------------------- */
    var counters = document.querySelectorAll("[data-counter]");
    if (counters.length && "IntersectionObserver" in window) {
        var counterObserver = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    var el = entry.target;
                    var target = parseInt(el.getAttribute("data-counter"), 10) || 0;
                    var step = Math.max(1, Math.ceil(target / 60));
                    var count = 0;

                    (function tick() {
                        count += step;
                        if (count >= target) {
                            el.textContent = target;
                        } else {
                            el.textContent = count;
                            requestAnimationFrame(tick);
                        }
                    })();

                    counterObserver.unobserve(el);
                }
            });
        }, { threshold: 0.5 });

        counters.forEach(function (c) { counterObserver.observe(c); });
    }


    /* -----------------------------------------
        5) TYPEWRITER TEXT EFFECT
        Usage in HTML:
        <span data-typewriter="Welcome to Bethak Cafe"></span>
    ----------------------------------------- */
    document.querySelectorAll("[data-typewriter]").forEach(function (el) {
        var text = el.getAttribute("data-typewriter");
        el.textContent = "";

        function typeIt() {
            var i = 0;
            (function type() {
                if (i < text.length) {
                    el.textContent += text.charAt(i);
                    i++;
                    setTimeout(type, 60);
                }
            })();
        }

        if ("IntersectionObserver" in window) {
            var typeObserver = new IntersectionObserver(function (entries) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        typeIt();
                        typeObserver.unobserve(el);
                    }
                });
            }, { threshold: 0.5 });
            typeObserver.observe(el);
        } else {
            typeIt();
        }
    });

})();
