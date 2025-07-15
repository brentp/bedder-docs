// Move bed files section to sidebar above table of contents
document.addEventListener('DOMContentLoaded', function () {
    // Find the bed files div
    const bedFilesDiv = document.querySelector('.fixed-bed-files');

    // Find the secondary sidebar (where TOC is)
    const secondarySidebar = document.querySelector('.md-sidebar--secondary .md-sidebar__scrollwrap');

    if (bedFilesDiv && secondarySidebar) {
        // Move the bed files div to the beginning of the secondary sidebar
        secondarySidebar.insertBefore(bedFilesDiv, secondarySidebar.firstChild);
    }
}); 