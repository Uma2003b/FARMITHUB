const crops = [
    {
        crop: "Wheat",
        locations: {
            north: { sowing: 11, harvesting: 4 },
            south: { sowing: 10, harvesting: 3 },
            east: { sowing: 11, harvesting: 4 },
            west: { sowing: 11, harvesting: 4 }
        },
        description: "A staple cereal grain widely cultivated for its edible seeds. Best grown in temperate climates with well-drained soil.",
        tips: "Requires 100-150 frost-free days. Water regularly during tillering and heading stages."
    },
    {
        crop: "Rice",
        locations: {
            north: { sowing: 6, harvesting: 10 },
            south: { sowing: 5, harvesting: 9 },
            east: { sowing: 6, harvesting: 10 },
            west: { sowing: 6, harvesting: 10 }
        },
        description: "A water-loving grain crop that feeds half the world's population. Thrives in flooded fields.",
        tips: "Needs continuous flooding during growth. Transplant seedlings for better yield."
    },
    {
        crop: "Maize",
        locations: {
            north: { sowing: 5, harvesting: 9 },
            south: { sowing: 4, harvesting: 8 },
            east: { sowing: 5, harvesting: 9 },
            west: { sowing: 5, harvesting: 9 }
        },
        description: "Also known as corn, a versatile crop used for food, feed, and industrial purposes.",
        tips: "Plant after last frost. Requires full sun and consistent moisture during pollination."
    },
    {
        crop: "Barley",
        locations: {
            north: { sowing: 11, harvesting: 4 },
            south: { sowing: 10, harvesting: 3 },
            east: { sowing: 11, harvesting: 4 },
            west: { sowing: 11, harvesting: 4 }
        },
        description: "A hardy cereal grain used for food, animal feed, and brewing malt.",
        tips: "Cold-tolerant crop. Good for winter planting in mild climates."
    },
    {
        crop: "Sugarcane",
        locations: {
            north: { sowing: 2, harvesting: 12 },
            south: { sowing: 1, harvesting: 11 },
            east: { sowing: 2, harvesting: 12 },
            west: { sowing: 2, harvesting: 12 }
        },
        description: "A tall perennial grass grown for sugar production. Requires tropical or subtropical conditions.",
        tips: "Needs 12-18 months to mature. High water requirement throughout growth."
    },
    {
        crop: "Cotton",
        locations: {
            north: { sowing: 6, harvesting: 11 },
            south: { sowing: 5, harvesting: 10 },
            east: { sowing: 6, harvesting: 11 },
            west: { sowing: 6, harvesting: 11 }
        },
        description: "A fiber crop grown for its fluffy white bolls used in textile manufacturing.",
        tips: "Requires hot, dry climate. Boll weevils are a major pest concern."
    },
    {
        crop: "Groundnut",
        locations: {
            north: { sowing: 6, harvesting: 10 },
            south: { sowing: 5, harvesting: 9 },
            east: { sowing: 6, harvesting: 10 },
            west: { sowing: 6, harvesting: 10 }
        },
        description: "Also called peanuts, grown for their edible nuts and oil. Pods develop underground.",
        tips: "Plant in well-drained sandy soil. Harvest when leaves turn yellow."
    },
    {
        crop: "Soybean",
        locations: {
            north: { sowing: 6, harvesting: 9 },
            south: { sowing: 5, harvesting: 8 },
            east: { sowing: 6, harvesting: 9 },
            west: { sowing: 6, harvesting: 9 }
        },
        description: "A protein-rich legume crop used for food, feed, and oil production.",
        tips: "Nitrogen-fixing plant. Good rotation crop to improve soil fertility."
    },
    {
        crop: "Pulses",
        locations: {
            north: { sowing: 10, harvesting: 3 },
            south: { sowing: 9, harvesting: 2 },
            east: { sowing: 10, harvesting: 3 },
            west: { sowing: 10, harvesting: 3 }
        },
        description: "Includes lentils, chickpeas, and beans. Protein-rich legumes important for food security.",
        tips: "Winter crop in many regions. Helps fix nitrogen in soil."
    },
    {
        crop: "Mustard",
        locations: {
            north: { sowing: 10, harvesting: 2 },
            south: { sowing: 9, harvesting: 1 },
            east: { sowing: 10, harvesting: 2 },
            west: { sowing: 10, harvesting: 2 }
        },
        description: "An oilseed crop grown for its seeds used in cooking oil and condiments.",
        tips: "Cold-weather crop. Seeds used for both oil and spice production."
    },
    {
        crop: "Sunflower",
        locations: {
            north: { sowing: 1, harvesting: 4 },
            south: { sowing: 12, harvesting: 3 },
            east: { sowing: 1, harvesting: 4 },
            west: { sowing: 1, harvesting: 4 }
        },
        description: "Tall flowering plants grown for their edible seeds and oil.",
        tips: "Attracts pollinators. Requires full sun and well-drained soil."
    },
    {
        crop: "Jute",
        locations: {
            north: { sowing: 3, harvesting: 7 },
            south: { sowing: 2, harvesting: 6 },
            east: { sowing: 3, harvesting: 7 },
            west: { sowing: 3, harvesting: 7 }
        },
        description: "A fiber crop used for making burlap, sacks, and other coarse fabrics.",
        tips: "Grows well in hot, humid conditions. Requires plenty of water."
    }
];


const months = ["Crop", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

// Get current month for highlighting
const currentMonthIndex = new Date().getMonth() + 1; // 1-12


function renderCalendar(filter = "all", searchTerm = "", location = "north") {
    const calendar = document.getElementById("calendar");

    // Show loading state
    showLoadingState(calendar);

    // Simulate loading delay for smooth transition
    setTimeout(() => {
        renderCalendarContent(filter, searchTerm, location);
    }, 300);
}

function showLoadingState(calendar) {
    calendar.innerHTML = `
        <div class="calendar-loading" style="grid-column: 1 / -1;">
            <div class="loading-spinner"></div>
            <div class="loading-text">Loading crop calendar...</div>
        </div>
    `;
}

function renderCalendarContent(filter = "all", searchTerm = "", location = "north") {
    const calendar = document.getElementById("calendar");
    calendar.innerHTML = "";

    // Header Row with staggered animation
    months.forEach((month, index) => {
        const div = document.createElement("div");
        div.className = "month";
        if (index === currentMonthIndex) {
            div.classList.add("current-month");
        }
        div.innerText = month;
        div.style.animationDelay = `${index * 0.05}s`;
        calendar.appendChild(div);
    });

    // Filter crops
    let filteredCrops = crops.filter(crop => filter === "all" || crop.crop === filter);

    // Apply search filter
    if (searchTerm) {
        filteredCrops = filteredCrops.filter(crop =>
            crop.crop.toLowerCase().includes(searchTerm.toLowerCase()) ||
            crop.description.toLowerCase().includes(searchTerm.toLowerCase())
        );
    }

    // Render crops with staggered animation
    filteredCrops.forEach((crop, cropIndex) => {
        const row = [crop.crop, ...Array(12).fill("")];
        const locData = crop.locations[location];
        const start = locData.sowing;
        const end = locData.harvesting < start ? locData.harvesting + 12 : locData.harvesting;

        for (let i = start; i <= end; i++) {
            const monthIndex = i > 12 ? i - 12 : i;

            if (i === start) {
                row[monthIndex] = "sow";
            } else if (i === end) {
                row[monthIndex] = "harvest";
            } else {
                row[monthIndex] = "grow";
            }
        }

        row.forEach((cell, idx) => {
            const div = document.createElement("div");
            const animationDelay = (cropIndex * 0.1) + (idx * 0.02);
            div.style.animationDelay = `${animationDelay}s`;

            if (idx === 0) {
                div.className = "crop-name";
                div.innerText = crop.crop;
                div.setAttribute('role', 'rowheader');
                div.setAttribute('aria-label', `${crop.crop} crop row`);
            } else {
                div.className = `month-cell ${cell}`;
                div.setAttribute('role', 'gridcell');
                
                if (cell === "sow") {
                    div.innerHTML = `
                        <span class="emoji" role="img" aria-label="planting">🌱</span>
                        <div class="tooltip">Sowing season for ${crop.crop}</div>
                    `;
                    div.setAttribute('aria-label', `${crop.crop} sowing month`);
                    addCellInteractions(div, crop.crop, 'sowing');
                } else if (cell === "harvest") {
                    div.innerHTML = `
                        <span class="emoji" role="img" aria-label="harvesting">🌾</span>
                        <div class="tooltip">Harvesting season for ${crop.crop}</div>
                    `;
                    div.setAttribute('aria-label', `${crop.crop} harvesting month`);
                    addCellInteractions(div, crop.crop, 'harvesting');
                } else if (cell === "grow") {
                    div.innerHTML = `
                        <span class="emoji" role="img" aria-label="growing">🟩</span>
                        <div class="tooltip">Growing season for ${crop.crop}</div>
                    `;
                    div.setAttribute('aria-label', `${crop.crop} growing period`);
                    addCellInteractions(div, crop.crop, 'growing');
                }
            }

            calendar.appendChild(div);
        });
    });
}

function addCellInteractions(div, cropName, phase) {
    div.addEventListener("mouseenter", (e) => {
        e.target.style.transform = "translateY(-2px) scale(1.05)";
        e.target.style.zIndex = "10";
        
        // Show tooltip
        const tooltip = e.target.querySelector('.tooltip');
        if (tooltip) {
            tooltip.style.visibility = 'visible';
            tooltip.style.opacity = '1';
        }
    });

    div.addEventListener("mouseleave", (e) => {
        e.target.style.transform = "";
        e.target.style.zIndex = "";
        
        // Hide tooltip
        const tooltip = e.target.querySelector('.tooltip');
        if (tooltip) {
            tooltip.style.visibility = 'hidden';
            tooltip.style.opacity = '0';
        }
    });

    div.addEventListener("click", (e) => {
        // Add click feedback
        div.style.transform = "scale(0.95)";
        setTimeout(() => {
            div.style.transform = "";
        }, 150);

        // Show detailed info in modal
        showCropModal(cropName, phase);
    });
}

// Enhanced dropdown event handler with smooth transitions
document.getElementById("cropSelect").addEventListener("change", function () {
    const selectedCrop = this.value;
    const searchTerm = document.getElementById("cropSearch").value;
    const location = document.getElementById("locationSelect").value;
    const calendar = document.getElementById("calendar");

    // Add fade out effect
    calendar.style.opacity = "0.5";
    calendar.style.transform = "translateY(10px)";

    setTimeout(() => {
        renderCalendar(selectedCrop, searchTerm, location);

        // Fade back in
        setTimeout(() => {
            calendar.style.opacity = "1";
            calendar.style.transform = "translateY(0)";
        }, 100);
    }, 200);
});

// Enhanced location dropdown event handler
document.getElementById("locationSelect").addEventListener("change", function () {
    const selectedLocation = this.value;
    const selectedCrop = document.getElementById("cropSelect").value;
    const searchTerm = document.getElementById("cropSearch").value;
    const calendar = document.getElementById("calendar");

    // Add fade out effect
    calendar.style.opacity = "0.5";
    calendar.style.transform = "translateY(10px)";

    setTimeout(() => {
        renderCalendar(selectedCrop, searchTerm, selectedLocation);

        // Fade back in
        setTimeout(() => {
            calendar.style.opacity = "1";
            calendar.style.transform = "translateY(0)";
        }, 100);
    }, 200);
});

// Add keyboard navigation for accessibility
document.getElementById("cropSelect").addEventListener("keydown", function(e) {
    if (e.key === "Enter" || e.key === " ") {
        this.click();
    }
});

document.getElementById("locationSelect").addEventListener("keydown", function(e) {
    if (e.key === "Enter" || e.key === " ") {
        this.click();
    }
});

// Modal functionality
function showCropModal(cropName, phase) {
    const crop = crops.find(c => c.crop === cropName);
    if (!crop) return;

    const modal = document.getElementById("cropModal");
    const modalTitle = document.getElementById("modalTitle");
    const modalBody = document.getElementById("modalBody");

    modalTitle.textContent = `${crop.crop} - ${phase.charAt(0).toUpperCase() + phase.slice(1)} Phase`;

    const phaseInfo = getPhaseInfo(phase, crop);
    modalBody.innerHTML = `
        <p><strong>Description:</strong> ${crop.description}</p>
        <p><strong>Growing Tips:</strong> ${crop.tips}</p>
        <div style="margin-top: 1rem; padding: 1rem; background: var(--bg-secondary); border-radius: 8px;">
            <strong>${phase.charAt(0).toUpperCase() + phase.slice(1)} Information:</strong><br>
            ${phaseInfo}
        </div>
    `;

    modal.style.display = "block";

    // Close modal when clicking outside
    modal.addEventListener("click", function(e) {
        if (e.target === modal) {
            modal.style.display = "none";
        }
    });
}

function getPhaseInfo(phase, crop) {
    const monthNames = ["January", "February", "March", "April", "May", "June",
                       "July", "August", "September", "October", "November", "December"];

    switch(phase) {
        case 'sowing':
            return `Start planting in ${monthNames[crop.sowing - 1]}. Prepare soil well and ensure proper seed depth.`;
        case 'growing':
            return `Monitor growth regularly. Water consistently and watch for pests. This phase typically lasts 2-4 months.`;
        case 'harvesting':
            return `Harvest begins in ${monthNames[crop.harvesting - 1]}. Check for maturity signs and harvest at optimal time for best quality.`;
        default:
            return "General growing information for this crop.";
    }
}

// Close modal functionality
document.addEventListener("DOMContentLoaded", function() {
    const closeBtn = document.querySelector(".close");
    if (closeBtn) {
        closeBtn.addEventListener("click", function() {
            document.getElementById("cropModal").style.display = "none";
        });
    }
});

// Search functionality
let searchTimeout;
document.getElementById("cropSearch").addEventListener("input", function(e) {
    clearTimeout(searchTimeout);
    const searchTerm = e.target.value;

    searchTimeout = setTimeout(() => {
        const selectedCrop = document.getElementById("cropSelect").value;
        const location = document.getElementById("locationSelect").value;
        renderCalendar(selectedCrop, searchTerm, location);
    }, 300);
});

// Reset button functionality
document.getElementById("resetBtn").addEventListener("click", function() {
    document.getElementById("locationSelect").value = "north";
    document.getElementById("cropSelect").value = "all";
    document.getElementById("cropSearch").value = "";
    renderCalendar("all", "", "north");
});

// Export functionality
document.getElementById("exportBtn").addEventListener("click", function() {
    exportCalendar();
});

function exportCalendar() {
    // Simple export as image (using html2canvas if available) or print
    if (window.html2canvas) {
        html2canvas(document.querySelector('.calendar')).then(canvas => {
            const link = document.createElement('a');
            link.download = 'crop-calendar.png';
            link.href = canvas.toDataURL();
            link.click();
        });
    } else {
        // Fallback to print
        window.print();
    }
}

// Initialize calendar with enhanced loading
document.addEventListener("DOMContentLoaded", function() {
    // Add initial loading state
    const calendar = document.getElementById("calendar");
    showLoadingState(calendar);

    // Load calendar after a brief delay
    setTimeout(() => {
        renderCalendar();
    }, 500);
});
