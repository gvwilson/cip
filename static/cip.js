// Open a tab.
function openTab(evt, language) {
  const pledges = document.getElementsByClassName("pledge")
  Array.from(pledges).forEach(p => {
    p.style.display = "none"
  })

  const tabcontrols = document.getElementsByClassName("tabcontrol")
  Array.from(tabcontrols).forEach(tc => {
    tc.className = tc.className.replace("active", "")
  })

  document.getElementById(language).style.display = "block"
  evt.currentTarget.className += " active"
}

// Open the default tab when the page loads.
window.onload = () => {
  document.getElementById("defaultLang").click()
}
