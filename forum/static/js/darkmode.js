document.addEventListener("DOMContentLoaded", () => {
  const htmlEl = document.getElementById("html-root");
  const toggleBtn = document.getElementById("theme-toggle");

  if (!htmlEl || !toggleBtn) {
    console.error("Theme toggle or HTML root element not found.");
    return;
  }

  const moonIcon = `
    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-yellow-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
        d="M21 12.79A9 9 0 0111.21 3a7 7 0 107.78 7.78A9.02 9.02 0 0121 12.79z" />
    </svg>`;

  const sunIcon = `
    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-yellow-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
        d="M12 3v1m0 16v1m8.66-10h-1M4.34 12h-1m15.07 6.07l-.71-.71M6.34 6.34l-.71-.71m12.02 0l-.71.71M6.34 17.66l-.71.71M12 7a5 5 0 100 10 5 5 0 000-10z" />
    </svg>`;

  // Set initial mode
  const storedTheme = localStorage.getItem("theme");
  console.log("Stored theme:", storedTheme);

  if (storedTheme === "dark") {
    htmlEl.classList.add("dark");
    toggleBtn.innerHTML = sunIcon;
  } else {
    htmlEl.classList.remove("dark");
    toggleBtn.innerHTML = moonIcon;
  }

  // Toggle
  toggleBtn.addEventListener("click", () => {
    const isDark = htmlEl.classList.toggle("dark");
    localStorage.setItem("theme", isDark ? "dark" : "light");
    toggleBtn.innerHTML = isDark ? sunIcon : moonIcon;

    console.log("Toggled theme:", isDark ? "dark" : "light");
    console.log("Current html classList:", htmlEl.classList.value);
  });
});
