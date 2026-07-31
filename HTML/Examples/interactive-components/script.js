const tabs = document.querySelectorAll(".tab");
const tabContents = document.querySelectorAll(".tab-content");

tabs.forEach((tab) => {
  tab.addEventListener("click", () => {
    tabs.forEach((item) => item.classList.remove("active"));
    tabContents.forEach((item) => item.classList.remove("active"));
    tabs.forEach((item) => item.setAttribute("aria-selected", "false"));
    tabContents.forEach((item) => {
      item.hidden = true;
    });

    tab.classList.add("active");
    tab.setAttribute("aria-selected", "true");
    const activeContent = document.getElementById(tab.dataset.tab);
    activeContent.hidden = false;
    activeContent.classList.add("active");
  });
});

const faqQuestions = document.querySelectorAll(".faq-question");

faqQuestions.forEach((question) => {
  question.addEventListener("click", () => {
    const answer = question.nextElementSibling;
    const isOpen = answer.classList.toggle("open");
    answer.hidden = !isOpen;
    question.setAttribute("aria-expanded", String(isOpen));
  });
});

const steps = document.querySelectorAll(".step");
const nextStepButton = document.getElementById("next-step");
let currentStep = 0;

nextStepButton.addEventListener("click", () => {
  currentStep = (currentStep + 1) % steps.length;
  steps.forEach((step, index) => {
    step.classList.toggle("active", index <= currentStep);
  });
});

const toast = document.getElementById("toast");
const showToastButton = document.getElementById("show-toast");

showToastButton.addEventListener("click", () => {
  toast.classList.add("show");
  setTimeout(() => {
    toast.classList.remove("show");
  }, 1800);
});
