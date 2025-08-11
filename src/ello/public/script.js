const alreadyExpanded = new WeakSet();
const alreadyCollapsed = new WeakSet();

function autoOpenSteps(element) {
  if (element.matches?.('button[id^="step-"]')) {
    tryExpand(element);
  }
  element.querySelectorAll?.('button[id^="step-"]').forEach((btn) => {
    tryExpand(btn);
  });
}

function tryExpand(btn) {
  const isClosed = btn.getAttribute('data-state') === 'closed';
  if (
    isClosed &&
    !alreadyExpanded.has(btn) &&
    btn.querySelector('svg.lucide-chevron-down')
  ) {
    btn.click();
    alreadyExpanded.add(btn);
  }
}

function collapseReasoningBlocks() {
  document.querySelectorAll('button').forEach((button) => {
    const buttonText = button.textContent?.trim();
    if (buttonText && buttonText.includes('Used Reasoning')) {
      const isExpanded = button.getAttribute('data-state') === 'open';
      
      if (isExpanded && !alreadyCollapsed.has(button)) {
        const reasoningContainer = button.parentElement?.querySelector('[data-state="open"]');
        if (reasoningContainer) {
          setTimeout(() => {
            if (button.getAttribute('data-state') === 'open') {
              button.click();
              alreadyCollapsed.add(button);
            }
          }, 2000); // 2 second delay
        }
      }
    }
  });
}

function removeCopyButtons() {
  document.querySelectorAll('button[data-state="closed"]').forEach((button) => {
    if (button.querySelector('.lucide-copy')) {
      button.remove();
    }
  });
}

removeCopyButtons();

const mutationObserver = new MutationObserver((mutationList) => {
  for (const mutation of mutationList) {
    if (mutation.type === 'childList') {
      for (const node of mutation.addedNodes) {
        if (node.nodeType === Node.ELEMENT_NODE) {
          autoOpenSteps(node);
          setTimeout(() => collapseReasoningBlocks(), 3000);
        }
      }
    }
  }
});

mutationObserver.observe(document.body, {
  childList: true,
  subtree: true,
});

const copyButtonObserver = new MutationObserver(() => {
  removeCopyButtons();
});

copyButtonObserver.observe(document.body, {
  childList: true,
  subtree: true,
});

document.querySelectorAll('button[id^="step-"]').forEach(autoOpenSteps);

setTimeout(() => collapseReasoningBlocks(), 3000);
