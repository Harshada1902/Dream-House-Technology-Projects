// ================= SCROLL ANIMATION =================
const fadeElements = document.querySelectorAll('.fade-up');

const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('show');
    }
  });
}, { threshold: 0.2 });

fadeElements.forEach(el => observer.observe(el));


// ================= COOKIE BANNER (EVERY TIME) =================
document.addEventListener("DOMContentLoaded", () => {
  const banner = document.getElementById("cookie-banner");
  const acceptBtn = document.getElementById("accept-cookies");
  const declineBtn = document.getElementById("decline-cookies");

  if (!banner || !acceptBtn || !declineBtn) return;

  acceptBtn.addEventListener("click", () => {
    banner.remove();   // remove banner on click
  });

  declineBtn.addEventListener("click", () => {
    banner.remove();   // remove banner on click
  });
});
