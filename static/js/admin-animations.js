/*=========================================
    BETHAK CAFE - ADMIN PANEL ANIMATIONS
    (self-contained: injects its own CSS,
    no changes needed in any .css file)

    Mirrors the animation style used on the
    customer side (all-animations.js) so the
    admin panel feels consistent with it:
      - scroll reveal for cards/tables
      - button ripple on click
      - counter-up numbers on stat cards
      - sidebar / page load animations
      - form shake on invalid fields
      - lightweight toast feedback + demo
        actions for buttons that don't have
        a dedicated page (Approve/Reject/
        Block/Delete/Mark Paid/etc.)
      - mobile sidebar toggle
=========================================*/

(function () {
    "use strict";

    /* -----------------------------------------
        0) INJECT REQUIRED CSS (once)
    ----------------------------------------- */
    var style = document.createElement("style");
    style.textContent =
        /* page fade-in */
        "body{animation:adminPageFade .6s ease;}" +
        "@keyframes adminPageFade{from{opacity:0;}to{opacity:1;}}" +

        /* sidebar brand glow */
        ".sidebar .gold,.sidebar .brand{animation:adminLogoGlow 3s infinite;}" +
        "@keyframes adminLogoGlow{0%{filter:drop-shadow(0 0 0px #D4AF37);}50%{filter:drop-shadow(0 0 10px #D4AF37);}100%{filter:drop-shadow(0 0 0px #D4AF37);}}" +

        /* sidebar links stagger in */
        ".sidebar .nav-link,.sidebar li{opacity:0;transform:translateX(-20px);animation:adminNavIn .5s ease forwards;}" +
        "@keyframes adminNavIn{to{opacity:1;transform:translateX(0);}}" +

        /* scroll reveal */
        ".admin-reveal{opacity:0;transform:translateY(30px);transition:opacity .6s ease,transform .6s ease;}" +
        ".admin-reveal.in-view{opacity:1;transform:translateY(0);}" +

        /* card hover lift */
        ".card{transition:transform .3s ease,box-shadow .3s ease;}" +
        ".card:hover{transform:translateY(-4px);box-shadow:0 10px 25px rgba(212,175,55,.15);}" +

        /* card-link-wrap (dashboard stat cards that are clickable) */
        "a.card-link-wrap{text-decoration:none;display:block;}" +

        /* ripple */
        ".admin-ripple{position:absolute;border-radius:50%;background:rgba(255,255,255,.5);transform:scale(0);animation:adminRipple .6s linear;pointer-events:none;}" +
        "@keyframes adminRipple{to{transform:scale(4);opacity:0;}}" +

        /* shake on invalid */
        ".admin-shake{animation:adminShake .4s ease;}" +
        "@keyframes adminShake{0%,100%{transform:translateX(0);}20%,60%{transform:translateX(-8px);}40%,80%{transform:translateX(8px);}}" +

        /* row fade out (delete) */
        ".admin-row-out{transition:opacity .35s ease,transform .35s ease;opacity:0;transform:translateX(30px);}" +

        /* status badge pop */
        ".admin-badge-pop{animation:adminBadgePop .4s ease;}" +
        "@keyframes adminBadgePop{0%{transform:scale(.6);opacity:0;}100%{transform:scale(1);opacity:1;}}" +

        /* toast */
        "#adminToastWrap{position:fixed;top:20px;right:20px;z-index:2000;display:flex;flex-direction:column;gap:10px;}" +
        ".admin-toast{background:#1b1b1b;border:1px solid #D4AF37;color:#fff;padding:12px 18px;border-radius:10px;min-width:220px;box-shadow:0 8px 20px rgba(0,0,0,.4);opacity:0;transform:translateX(40px);transition:opacity .35s ease,transform .35s ease;font-size:14px;}" +
        ".admin-toast.show{opacity:1;transform:translateX(0);}" +
        ".admin-toast strong{color:#D4AF37;}" +

        /* mobile sidebar */
        "@media(max-width:768px){.sidebar{left:-260px;top:0;transition:left .3s ease;z-index:1050;}.sidebar.show{left:0;}}";
    document.head.appendChild(style);


    /* -----------------------------------------
        1) MOBILE SIDEBAR TOGGLE
    ----------------------------------------- */
    var toggleBtn = document.getElementById("sidebarToggle");
    var sidebarEl = document.querySelector(".sidebar");
    if (toggleBtn && sidebarEl) {
        toggleBtn.addEventListener("click", function () {
            sidebarEl.classList.toggle("show");
        });
    }


    /* -----------------------------------------
        2) SIDEBAR LINKS - STAGGERED ENTRANCE
    ----------------------------------------- */
    var navItems = document.querySelectorAll(".sidebar .nav-link, .sidebar li");
    navItems.forEach(function (el, i) {
        el.style.animationDelay = (i * 0.06) + "s";
    });


    /* -----------------------------------------
        3) SCROLL REVEAL FOR CARDS / TABLES
    ----------------------------------------- */
    var revealSelectors = [
        ".card", ".table-box", ".table-responsive",
        ".table-wrap", ".avatar", ".preview"
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
        }, { threshold: 0.1 });

        revealEls.forEach(function (el) {
            el.classList.add("admin-reveal");
            revealObserver.observe(el);
        });
    }


    /* -----------------------------------------
        4) BUTTON RIPPLE (click animation)
        Applies to all Bootstrap buttons + links
        styled as buttons across the admin panel.
    ----------------------------------------- */
    var rippleSelectors = ".btn";
    document.querySelectorAll(rippleSelectors).forEach(function (btn) {
        var computedPos = window.getComputedStyle(btn).position;
        if (computedPos === "static") btn.style.position = "relative";
        btn.style.overflow = "hidden";

        btn.addEventListener("click", function (e) {
            var rect = btn.getBoundingClientRect();
            var size = Math.max(rect.width, rect.height);
            var circle = document.createElement("span");
            circle.className = "admin-ripple";
            circle.style.width = circle.style.height = size + "px";
            circle.style.left = (e.clientX - rect.left - size / 2) + "px";
            circle.style.top = (e.clientY - rect.top - size / 2) + "px";
            btn.appendChild(circle);
            setTimeout(function () { circle.remove(); }, 600);
        });
    });


    /* -----------------------------------------
        5) FORM SHAKE ON INVALID FIELD
    ----------------------------------------- */
    document.querySelectorAll("form").forEach(function (form) {
        form.querySelectorAll("input[required], select[required], textarea[required]")
            .forEach(function (field) {
                field.addEventListener("invalid", function () {
                    var wrapper = field.closest(".mb-3") || field;
                    wrapper.classList.remove("admin-shake");
                    void wrapper.offsetWidth; // restart animation
                    wrapper.classList.add("admin-shake");
                });
            });
    });


    /* -----------------------------------------
        6) COUNTER-UP FOR STAT NUMBERS
        Auto-detects numbers inside .card h2/h3
        (handles ₹ prefix and Indian comma format)
    ----------------------------------------- */
    var statEls = document.querySelectorAll(".card h2, .card h3");
    if (statEls.length && "IntersectionObserver" in window) {
        var counterObserver = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (!entry.isIntersecting) return;
                var el = entry.target;
                var raw = el.textContent.trim();
                var match = raw.match(/^([^\d]*)([\d,]+)([^\d]*)$/);
                if (!match) { counterObserver.unobserve(el); return; }

                var prefix = match[1];
                var numStr = match[2].replace(/,/g, "");
                var suffix = match[3];
                var target = parseInt(numStr, 10);
                if (isNaN(target)) { counterObserver.unobserve(el); return; }

                var step = Math.max(1, Math.ceil(target / 40));
                var count = 0;

                (function tick() {
                    count += step;
                    if (count >= target) {
                        el.textContent = prefix + target.toLocaleString("en-IN") + suffix;
                    } else {
                        el.textContent = prefix + count.toLocaleString("en-IN") + suffix;
                        requestAnimationFrame(tick);
                    }
                })();

                counterObserver.unobserve(el);
            });
        }, { threshold: 0.4 });

        statEls.forEach(function (el) { counterObserver.observe(el); });
    }


    /* -----------------------------------------
        7) TOAST NOTIFICATION SYSTEM
    ----------------------------------------- */
    var toastWrap = document.getElementById("adminToastWrap");
    if (!toastWrap) {
        toastWrap = document.createElement("div");
        toastWrap.id = "adminToastWrap";
        document.body.appendChild(toastWrap);
    }

    function showToast(message) {
        var toast = document.createElement("div");
        toast.className = "admin-toast";
        toast.innerHTML = message;
        toastWrap.appendChild(toast);
        requestAnimationFrame(function () { toast.classList.add("show"); });
        setTimeout(function () {
            toast.classList.remove("show");
            setTimeout(function () { toast.remove(); }, 400);
        }, 2800);
    }
    window.adminShowToast = showToast;


    /* -----------------------------------------
        8) GENERIC "SAVE" FORMS
        (Add Menu, Edit Menu, Profile, Settings)
        - shows a success toast
        - redirects if data-redirect is set
    ----------------------------------------- */
    document.querySelectorAll(".save-food-form").forEach(function (form) {
        form.addEventListener("submit", function (e) {
            e.preventDefault();
            var msg = form.getAttribute("data-success-msg") || "Saved successfully!";
            showToast("<strong>Success:</strong> " + msg);
            var redirect = form.getAttribute("data-redirect");
            if (redirect) {
                setTimeout(function () { window.location.href = redirect; }, 900);
            }
        });
    });

    document.querySelectorAll(".delete-food-btn").forEach(function (btn) {
        btn.addEventListener("click", function () {
            if (!confirm("Are you sure you want to delete this item?")) return;
            showToast("<strong>Deleted:</strong> Food item removed.");
            var redirect = btn.getAttribute("data-redirect");
            if (redirect) {
                setTimeout(function () { window.location.href = redirect; }, 900);
            }
        });
    });


    /* -----------------------------------------
        9) TABLE ROW ACTION BUTTONS
        (View / Edit / Delete / Approve / Reject
        / Complete / Block / Mark Paid / Download)
        Gives instant visual feedback for demo
        buttons that have no dedicated backend.
    ----------------------------------------- */
    var statusMap = {
        "approve":    { text: "Approved",  cls: "bg-success" },
        "reject":     { text: "Rejected",  cls: "bg-danger"  },
        "complete":   { text: "Completed", cls: "bg-success" },
        "mark paid":  { text: "Paid",      cls: "bg-success" }
    };

    document.addEventListener("click", function (e) {
        var btn = e.target.closest(".table-box .btn, .table-responsive .btn, .table-wrap .btn");
        if (!btn) return;
        if (btn.classList.contains("delete-food-btn")) return; // handled above
        if (btn.tagName === "A" && btn.getAttribute("href") && btn.getAttribute("href") !== "#") return; // real navigation link

        var label = btn.textContent.trim().toLowerCase();
        var row = btn.closest("tr");

        /* DELETE (generic rows: customers, employees, inventory) */
        if (label === "delete") {
            e.preventDefault();
            if (!confirm("Are you sure you want to delete this row?")) return;
            if (row) {
                row.classList.add("admin-row-out");
                setTimeout(function () { row.remove(); }, 350);
            }
            showToast("<strong>Deleted</strong> successfully.");
            return;
        }

        /* BLOCK toggle (customers) */
        if (label === "block" || label === "unblock") {
            e.preventDefault();
            var badge = row ? row.querySelector(".badge") : null;
            if (badge) {
                var blocked = badge.textContent.trim().toLowerCase() === "blocked";
                badge.textContent = blocked ? "Active" : "Blocked";
                badge.className = "badge " + (blocked ? "bg-success" : "bg-secondary") + " admin-badge-pop";
            }
            btn.textContent = btn.textContent.trim().toLowerCase() === "block" ? "Unblock" : "Block";
            showToast("Customer status updated.");
            return;
        }

        /* Known status-changing actions */
        if (statusMap[label]) {
            e.preventDefault();
            var info = statusMap[label];
            var badge2 = row ? row.querySelector(".badge") : null;
            if (badge2) {
                badge2.textContent = info.text;
                badge2.className = "badge " + info.cls + " admin-badge-pop";
            }
            btn.disabled = true;
            btn.classList.add("disabled");
            showToast("<strong>" + info.text + ":</strong> status updated.");
            return;
        }

        /* View / other read-only actions */
        if (label === "view") {
            e.preventDefault();
            var idCell = row ? row.querySelector("td") : null;
            showToast("Viewing details" + (idCell ? " for <strong>" + idCell.textContent.trim() + "</strong>" : "") + ".");
            return;
        }

        /* Download PDF / Excel (reports page) */
        if (label.indexOf("download") === 0) {
            e.preventDefault();
            showToast("<strong>" + btn.textContent.trim() + "</strong> started...");
            return;
        }

        /* Search / Filter / + Add Item buttons without a backend */
        if (label === "search" || label === "filter" || label.indexOf("add item") !== -1) {
            e.preventDefault();
            showToast(btn.textContent.trim() + " applied.");
            return;
        }
    });

})();

