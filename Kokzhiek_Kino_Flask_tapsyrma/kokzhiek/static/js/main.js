(function () {
  "use strict";

  const NBSP = " ";

  function formatMoney(value) {
    return String(Math.round(value)).replace(/\B(?=(\d{3})+(?!\d))/g, NBSP) + NBSP + "₸";
  }

  function initNavigation() {
    const toggle = document.querySelector("[data-nav-toggle]");
    const nav = document.querySelector("[data-nav]");
    if (!toggle || !nav) {
      return;
    }
    toggle.addEventListener("click", () => {
      const open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", String(open));
    });
  }

  function initAlerts() {
    document.querySelectorAll("[data-dismiss]").forEach((button) => {
      button.addEventListener("click", () => {
        const alert = button.closest(".alert");
        if (alert) {
          alert.remove();
        }
      });
    });
  }

  function initPrint() {
    document.querySelectorAll("[data-print]").forEach((button) => {
      button.addEventListener("click", () => window.print());
    });
  }

  function initOrderForm() {
    const form = document.querySelector("[data-order-form]");
    if (!form) {
      return;
    }
    const max = Number(form.dataset.max);
    const price = Number(form.dataset.price);
    const reduced = Number(form.dataset.discountPrice);
    const seats = Array.from(form.querySelectorAll("input[name='seats']"));
    const list = form.querySelector("[data-selected-list]");
    const discounted = form.querySelector("input[name='discounted']");
    const total = form.querySelector("[data-total]");
    const submit = form.querySelector("[data-submit]");

    const update = () => {
      const chosen = seats.filter((seat) => seat.checked);
      const full = chosen.length >= max;
      seats.forEach((seat) => {
        if (!seat.checked && !seat.defaultDisabled) {
          seat.disabled = full;
        }
        seat.closest(".seat").classList.toggle("is-limit", full);
      });

      list.replaceChildren();
      if (!chosen.length) {
        const empty = document.createElement("li");
        empty.className = "placeholder";
        empty.textContent = "Әзірге орын таңдалмаған";
        list.append(empty);
      }
      chosen.forEach((seat) => {
        const [row, number] = seat.value.split("-");
        const item = document.createElement("li");
        item.textContent = row + "-қатар, " + number + "-орын";
        list.append(item);
      });

      discounted.max = String(chosen.length);
      if (Number(discounted.value) > chosen.length) {
        discounted.value = String(chosen.length);
      }
      const reducedCount = Math.max(0, Number(discounted.value) || 0);
      total.textContent = formatMoney((chosen.length - reducedCount) * price + reducedCount * reduced);
      submit.disabled = chosen.length === 0;
    };

    seats.forEach((seat) => {
      seat.defaultDisabled = seat.disabled;
    });
    form.addEventListener("change", update);
    discounted.addEventListener("input", update);
    update();
  }

  initNavigation();
  initAlerts();
  initPrint();
  initOrderForm();
})();
