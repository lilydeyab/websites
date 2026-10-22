
const properties = [
  {
    id: 1,
    title: "The Willow Residence",
    location: "Beverly Hills, Los Angeles",
    type: "villa",
    listing: "sale",
    price: 1250000,
    beds: 4,
    baths: 3,
    area: 2850,
    image: "photo-1600596542815-ffad4c1539a9",
    description: "A spacious contemporary residence with elegant interiors, generous living spaces and a beautifully landscaped outdoor area."
  },
  {
    id: 2,
    title: "The Urban Loft",
    location: "Downtown, New York",
    type: "apartment",
    listing: "rent",
    price: 3200,
    beds: 2,
    baths: 2,
    area: 1100,
    image: "photo-1600607687939-ce8a6c25118c",
    description: "A bright urban apartment with modern finishes, an open-plan layout and convenient access to city life."
  },
  {
    id: 3,
    title: "Oakwood Family House",
    location: "Austin, Texas",
    type: "house",
    listing: "sale",
    price: 485000,
    beds: 4,
    baths: 3,
    area: 2300,
    image: "photo-1600585154340-be6161a56a0c",
    description: "A welcoming family home with generous bedrooms, a functional layout and room to relax."
  },
  {
    id: 4,
    title: "The Olive Villa",
    location: "Scottsdale, Arizona",
    type: "villa",
    listing: "sale",
    price: 890000,
    beds: 5,
    baths: 4,
    area: 3200,
    image: "photo-1600607687920-4e2a09cf159d",
    description: "A refined villa with spacious interiors, private outdoor space and contemporary architectural details."
  },
  {
    id: 5,
    title: "Parkside Apartment",
    location: "Chicago, Illinois",
    type: "apartment",
    listing: "rent",
    price: 2400,
    beds: 2,
    baths: 1,
    area: 950,
    image: "photo-1600566753086-00f18fb6b3ea",
    description: "A comfortable, light-filled apartment with a practical floor plan and a convenient neighborhood location."
  },
  {
    id: 6,
    title: "The Cedar House",
    location: "Portland, Oregon",
    type: "house",
    listing: "sale",
    price: 620000,
    beds: 3,
    baths: 2,
    area: 1950,
    image: "photo-1600047509807-ba8f99d2cdde",
    description: "A stylish home combining warm materials, comfortable living areas and a peaceful residential setting."
  },
  {
    id: 7,
    title: "Skyline Penthouse",
    location: "Miami, Florida",
    type: "apartment",
    listing: "sale",
    price: 975000,
    beds: 3,
    baths: 3,
    area: 2100,
    image: "photo-1600607687644-c7171b42498f",
    description: "A sophisticated apartment with spacious rooms, clean finishes and an elevated city-living feel."
  },
  {
    id: 8,
    title: "Meadow Lane Home",
    location: "Nashville, Tennessee",
    type: "house",
    listing: "rent",
    price: 2800,
    beds: 3,
    baths: 2,
    area: 1750,
    image: "photo-1600566753190-17f0baa2a6c3",
    description: "A welcoming rental home with practical living spaces, comfortable bedrooms and a relaxed atmosphere."
  },
  {
    id: 9,
    title: "The Grand Estate",
    location: "Greenwich, Connecticut",
    type: "villa",
    listing: "sale",
    price: 1850000,
    beds: 5,
    baths: 4,
    area: 4100,
    image: "photo-1600607687939-ce8a6c25118c",
    description: "A spacious estate with elegant living areas, multiple bedrooms and an impressive modern design."
  }
];

const propertyGrid = document.getElementById("propertyGrid");
const searchForm = document.getElementById("searchForm");
const locationInput = document.getElementById("locationInput");
const typeFilter = document.getElementById("typeFilter");
const listingFilter = document.getElementById("listingFilter");
const sortFilter = document.getElementById("sortFilter");
const resultsMessage = document.getElementById("resultsMessage");

const propertyDialog = document.getElementById("propertyDialog");
const propertyDetails = document.getElementById("propertyDetails");
const dialogClose = document.getElementById("dialogClose");

const menuToggle = document.getElementById("menuToggle");
const navLinks = document.getElementById("navLinks");

const FAVORITES_KEY = "haven-property-favorites";

let favoriteIds = loadFavorites();

function loadFavorites() {
  try {
    const saved = JSON.parse(localStorage.getItem(FAVORITES_KEY) || "[]");

    if (!Array.isArray(saved)) return [];

    return saved.filter(id =>
      Number.isInteger(id) &&
      properties.some(property => property.id === id)
    );
  } catch {
    return [];
  }
}

function saveFavorites() {
  try {
    localStorage.setItem(FAVORITES_KEY, JSON.stringify(favoriteIds));
  } catch {
    console.warn("Favorites could not be saved in this browser.");
  }
}

function formatPrice(price, listing) {
  const formatted = new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0
  }).format(price);

  return listing === "rent"
    ? `${formatted} / month`
    : formatted;
}

function getImageUrl(imageId, width = 900) {
  return `https://images.unsplash.com/${imageId}?auto=format&fit=crop&w=${width}&q=80`;
}

function createPropertyCard(property) {
  const isFavorite = favoriteIds.includes(property.id);

  return `
    <article class="property-card">
      <div class="property-image">
        <img
          src="${getImageUrl(property.image)}"
          alt="${property.title}"
          loading="lazy"
        >

        <span class="property-badge">
          ${property.listing === "sale" ? "FOR SALE" : "FOR RENT"}
        </span>

        <button
          class="favorite-button ${isFavorite ? "is-favorite" : ""}"
          data-favorite="${property.id}"
          type="button"
          aria-label="${isFavorite ? "Remove from" : "Add to"} favorites"
          aria-pressed="${isFavorite}"
        >${isFavorite ? "♥" : "♡"}</button>
      </div>

      <div class="property-info">
        <p class="property-price">
          ${formatPrice(property.price, property.listing)}
        </p>

        <h3 class="property-title">${property.title}</h3>

        <p class="property-location">⌖ ${property.location}</p>

        <div class="property-meta">
          <span>${property.beds} Beds</span>
          <span>${property.baths} Baths</span>
          <span>${property.area.toLocaleString("en-US")} sq ft</span>
        </div>

        <button
          class="property-details-button"
          data-details="${property.id}"
          type="button"
        >View property details ↗</button>
      </div>
    </article>
  `;
}

function getFilteredProperties() {
  const location = locationInput.value.trim().toLowerCase();
  const type = typeFilter.value;
  const listing = listingFilter.value;
  const sort = sortFilter.value;

  const filtered = properties.filter(property => {
    const matchesLocation =
      `${property.location} ${property.title}`
        .toLowerCase()
        .includes(location);

    const matchesType =
      type === "all" || property.type === type;

    const matchesListing =
      listing === "all" || property.listing === listing;

    return matchesLocation && matchesType && matchesListing;
  });

  if (sort === "low-high") {
    filtered.sort((a, b) => a.price - b.price);
  } else if (sort === "high-low") {
    filtered.sort((a, b) => b.price - a.price);
  }

  return filtered;
}

function renderProperties() {
  const filtered = getFilteredProperties();

  if (filtered.length === 0) {
    propertyGrid.innerHTML = `
      <div class="empty-state">
        <h3>No properties found</h3>
        <p>Try another location or adjust your filters.</p>
      </div>
    `;
  } else {
    propertyGrid.innerHTML = filtered
      .map(createPropertyCard)
      .join("");
  }

  resultsMessage.textContent =
    `Showing ${filtered.length} of ${properties.length} properties`;
}

function openPropertyDetails(id) {
  const property = properties.find(item => item.id === id);

  if (!property) return;

  propertyDetails.innerHTML = `
    <img
      src="${getImageUrl(property.image, 1100)}"
      alt="${property.title}"
    >

    <p class="eyebrow">
      ${property.listing === "sale" ? "PROPERTY FOR SALE" : "PROPERTY FOR RENT"}
    </p>

    <h2>${property.title}</h2>

    <p>⌖ ${property.location}</p>

    <h3 class="property-price">
      ${formatPrice(property.price, property.listing)}
    </h3>

    <p>
      ${property.beds} bedrooms · ${property.baths} bathrooms
      · ${property.area.toLocaleString("en-US")} sq ft
    </p>

    <p>${property.description}</p>

    <a
      class="primary-button"
      href="mailto:hello@example.com?subject=${encodeURIComponent(
        "Property inquiry: " + property.title
      )}"
    >Ask about this property ↗</a>

    <p>
      <small>Demo listing. Replace this content and contact email with verified client information.</small>
    </p>
  `;

  if (typeof propertyDialog.showModal === "function") {
    propertyDialog.showModal();
  } else {
    propertyDialog.setAttribute("open", "");
  }
}

propertyGrid.addEventListener("click", event => {
  const favoriteButton = event.target.closest("[data-favorite]");
  const detailsButton = event.target.closest("[data-details]");

  if (favoriteButton) {
    const id = Number(favoriteButton.dataset.favorite);

    if (favoriteIds.includes(id)) {
      favoriteIds = favoriteIds.filter(item => item !== id);
    } else {
      favoriteIds.push(id);
    }

    saveFavorites();
    renderProperties();
    return;
  }

  if (detailsButton) {
    openPropertyDetails(Number(detailsButton.dataset.details));
  }
});

searchForm.addEventListener("submit", event => {
  event.preventDefault();
  renderProperties();

  document.getElementById("properties").scrollIntoView({
    behavior: "smooth"
  });
});

typeFilter.addEventListener("change", renderProperties);
listingFilter.addEventListener("change", renderProperties);
sortFilter.addEventListener("change", renderProperties);

locationInput.addEventListener("input", renderProperties);

dialogClose.addEventListener("click", () => {
  if (typeof propertyDialog.close === "function") {
    propertyDialog.close();
  } else {
    propertyDialog.removeAttribute("open");
  }
});

propertyDialog.addEventListener("click", event => {
  if (event.target === propertyDialog) {
    propertyDialog.close();
  }
});

menuToggle.addEventListener("click", () => {
  const isOpen = navLinks.classList.toggle("is-open");

  menuToggle.setAttribute("aria-expanded", String(isOpen));
  menuToggle.textContent = isOpen ? "✕" : "☰";
});

navLinks.addEventListener("click", event => {
  if (event.target.closest("a")) {
    navLinks.classList.remove("is-open");
    menuToggle.setAttribute("aria-expanded", "false");
    menuToggle.textContent = "☰";
  }
});

renderProperties();
