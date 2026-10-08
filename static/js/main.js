/*=========================================
    BETHAK CAFE - MAIN FUNCTIONAL JS
    (password show/hide, table selection)
    NOTE: This is separate from all-animations.js
    - all-animations.js  -> visual/decorative animations
    - main.js (this file) -> actual site functionality
=========================================*/

(function () {
    "use strict";

    /* -----------------------------------------
        1) PASSWORD SHOW / HIDE TOGGLE
        Works on login.html and register.html
        (any number of .password-box fields)
    ----------------------------------------- */
    document.querySelectorAll(".password-box").forEach(function (box) {
        var toggle = box.querySelector(".toggle-password");
        var input = box.querySelector("input");
        if (!toggle || !input) return;

        toggle.addEventListener("click", function () {
            var icon = toggle.querySelector("i");
            if (input.type === "password") {
                input.type = "text";
                if (icon) {
                    icon.classList.remove("bi-eye-fill");
                    icon.classList.add("bi-eye-slash-fill");
                }
            } else {
                input.type = "password";
                if (icon) {
                    icon.classList.remove("bi-eye-slash-fill");
                    icon.classList.add("bi-eye-fill");
                }
            }
        });
    });


    /* -----------------------------------------
        1B) PASSWORD STRENGTH METER
        (register.html - #password + .strength-bar/.strength-text)
    ----------------------------------------- */
    var pwField = document.getElementById("password");
    var strengthBar = document.querySelector(".strength-bar");
    var strengthText = document.querySelector(".strength-text");

    if (pwField && strengthBar && strengthText) {
        pwField.addEventListener("input", function () {
            var val = pwField.value;
            var score = 0;

            if (val.length >= 8) score++;
            if (/[a-z]/.test(val)) score++;
            if (/[A-Z]/.test(val)) score++;
            if (/[0-9]/.test(val)) score++;
            if (/[^A-Za-z0-9]/.test(val)) score++;

            var levels = [
                { width: "0%",   color: "#ff3b3b", text: "Password must contain at least 8 characters." },
                { width: "20%",  color: "#ff3b3b", text: "Very Weak" },
                { width: "40%",  color: "#ff3b3b", text: "Weak" },
                { width: "60%",  color: "#ffb020", text: "Medium" },
                { width: "80%",  color: "#8bc34a", text: "Strong" },
                { width: "100%", color: "#2ecc71", text: "Very Strong" }
            ];

            var level = val.length === 0 ? levels[0] : levels[score];

            strengthBar.style.width = level.width;
            strengthBar.style.background = level.color;
            strengthText.textContent = level.text;
        });
    }


    /* -----------------------------------------
        2) RESERVATION - TABLE SELECTION
        (reservation.html modal)
    ----------------------------------------- */
    var selectedTableSpan = document.getElementById("selectedTable");
    var tableCards = document.querySelectorAll(".table-card");
    var confirmBtn = document.querySelector(".confirm-table-btn");
    var chosenTable = null;

    if (tableCards.length) {
        tableCards.forEach(function (card) {
            card.addEventListener("click", function () {
                // booked tables can't be selected
                if (card.classList.contains("booked-table")) return;

                // clear previous selection
                tableCards.forEach(function (c) { c.classList.remove("active"); });

                // mark this one selected
                card.classList.add("active");
                chosenTable = card.getAttribute("data-table");
            });
        });
    }

    if (confirmBtn) {
        confirmBtn.addEventListener("click", function () {
            if (selectedTableSpan) {
                selectedTableSpan.textContent = chosenTable ? chosenTable : "None";
            }
            var hiddenInput = document.getElementById("hiddenSelectedTable");
            if (hiddenInput && chosenTable) {
                hiddenInput.value = chosenTable;
            }
        });
    }


    /* -----------------------------------------
        3) RESERVE BUTTON - block submit if no table chosen
    ----------------------------------------- */
    var reservationForm = document.querySelector(".reservation-card form");
    if (reservationForm) {
        reservationForm.addEventListener("submit", function (e) {
            if (!chosenTable) {
                e.preventDefault();
                alert("Please choose a table before reserving.");
            }
        });
    }

})();
