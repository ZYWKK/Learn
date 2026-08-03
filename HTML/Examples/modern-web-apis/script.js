class LearningTopic extends HTMLElement {
  static observedAttributes = ["level"];

  constructor() {
    super();
    const shadow = this.attachShadow({ mode: "open" });
    shadow.innerHTML = `
      <style>
        :host {
          display: block;
        }

        :host([hidden]) {
          display: none;
        }

        article {
          display: grid;
          gap: 16px;
          padding: 20px;
          border: 1px solid #cdd5cf;
          border-left: 5px solid #176b55;
          border-radius: 6px;
          background: #ffffff;
          color: #18211d;
        }

        .level {
          display: inline-flex;
          align-items: center;
          justify-content: center;
          width: 34px;
          height: 34px;
          margin-bottom: 12px;
          border-radius: 50%;
          background: #dcebe4;
          color: #176b55;
          font-size: 13px;
          font-weight: 800;
        }

        h3 {
          margin: 0 0 6px;
          font-size: 19px;
          line-height: 1.3;
          letter-spacing: 0;
        }

        .description {
          margin: 0;
          color: #5f6a64;
          line-height: 1.65;
        }

        .meta {
          align-self: end;
          padding-top: 12px;
          border-top: 1px solid #cdd5cf;
          color: #315f8d;
          font-size: 13px;
          font-weight: 700;
        }

        @container (min-width: 620px) {
          article {
            grid-template-columns: minmax(0, 1fr) minmax(190px, 0.34fr);
            align-items: center;
            padding: 24px 28px;
          }

          .copy {
            display: grid;
            grid-template-columns: 48px minmax(0, 1fr);
            column-gap: 12px;
          }

          .level {
            grid-row: 1 / 3;
            margin-bottom: 0;
          }

          .meta {
            padding: 0 0 0 18px;
            border-top: 0;
            border-left: 1px solid #cdd5cf;
          }
        }
      </style>
      <article>
        <div class="copy">
          <span class="level" aria-hidden="true"></span>
          <h3><slot name="title"></slot></h3>
          <p class="description"><slot></slot></p>
        </div>
        <div class="meta"><slot name="meta"></slot></div>
      </article>
    `;
  }

  connectedCallback() {
    this.renderLevel();
  }

  attributeChangedCallback() {
    this.renderLevel();
  }

  renderLevel() {
    const level = this.shadowRoot?.querySelector(".level");
    if (level) {
      level.textContent = this.getAttribute("level") || "--";
    }
  }
}

if (!customElements.get("learning-topic")) {
  customElements.define("learning-topic", LearningTopic);
}

const stage = document.querySelector("#component-stage");
const widthInput = document.querySelector("#stage-width");
const widthOutput = document.querySelector("#width-output");
const filterButtons = [...document.querySelectorAll("[data-filter]")];
const topics = [...document.querySelectorAll("learning-topic")];
const emptyState = document.querySelector("#empty-state");
const popover = document.querySelector("#api-popover");
const popoverButton = document.querySelector("#popover-button");
const supportList = document.querySelector("#support-list");

function updateStageWidth() {
  if (!stage || !widthInput || !widthOutput) {
    return;
  }

  const width = `${widthInput.value}px`;
  stage.style.setProperty("--stage-width", width);
  widthOutput.value = `${widthInput.value} px`;
}

function applyFilter(filter) {
  let visibleCount = 0;
  topics.forEach((topic) => {
    const visible = filter === "all" || topic.getAttribute("category") === filter;
    topic.hidden = !visible;
    visibleCount += visible ? 1 : 0;
  });

  filterButtons.forEach((button) => {
    button.setAttribute("aria-pressed", String(button.dataset.filter === filter));
  });

  if (emptyState) {
    emptyState.hidden = visibleCount > 0;
  }
}

function runViewUpdate(update) {
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (document.startViewTransition && !reduceMotion) {
    document.startViewTransition(update);
    return;
  }
  update();
}

function addSupportRow(label, supported) {
  if (!supportList) {
    return;
  }

  const item = document.createElement("li");
  const name = document.createElement("span");
  const state = document.createElement("strong");
  name.textContent = label;
  state.textContent = supported ? "支持" : "回退";
  state.className = supported ? "support-yes" : "support-no";
  item.append(name, state);
  supportList.append(item);
}

function setupSupportList() {
  addSupportRow("Custom Elements", "customElements" in window);
  addSupportRow("Container Queries", CSS.supports("container-type: inline-size"));
  addSupportRow("Popover API", "popover" in HTMLElement.prototype);
  addSupportRow("View Transitions", "startViewTransition" in document);
}

function setupPopover() {
  if (!popover || !popoverButton) {
    return;
  }

  const supportsPopover = "popover" in HTMLElement.prototype;
  popover.hidden = true;

  if (supportsPopover) {
    popover.hidden = false;
    popover.setAttribute("popover", "auto");
    popoverButton.setAttribute("popovertarget", popover.id);
    popover.addEventListener("toggle", (event) => {
      popoverButton.setAttribute("aria-expanded", String(event.newState === "open"));
    });
    return;
  }

  popoverButton.addEventListener("click", () => {
    popover.hidden = !popover.hidden;
    popoverButton.setAttribute("aria-expanded", String(!popover.hidden));
  });
}

widthInput?.addEventListener("input", updateStageWidth);
filterButtons.forEach((button) => {
  button.addEventListener("click", () => {
    runViewUpdate(() => applyFilter(button.dataset.filter || "all"));
  });
});

updateStageWidth();
setupSupportList();
setupPopover();
