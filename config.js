// =============================================================================
// 🌿 RESTAURANT & QR CODE CONFIGURATION SETTINGS
// =============================================================================
// Agar aapko kisi bhi doosre restaurant ya naye link ke liye ye setup use karna ho,
// toh aapko HTML/CSS code chhoone ki zaroorat nahi hai.
// BAS YAHAN NEECHE APNI DETAILS CHANGE KAREIN — SAB KUCH AUTOMATICALLY UPDATE HO JAYEGA!
// =============================================================================

const RESTAURANT_CONFIG = {
    // 1. Restaurant Basic Details
    restaurantName: "Olive Leaf",
    tagline: "Pure Vegetarian • Fine Dining",
    logoImage: "logo.png", // Folder me nayi image 'logo.png' naam se daalein

    // 2. Google Review Link & Text
    googleReviewLink: "https://share.google/CAuKpe2Po706mPhkI",
    googleRatingText: "Rate us on Google",
    googleRatingSubtext: "Your 5-star review means the world to us!",

    // 3. Instagram Link & Profile Handle
    instagramLink: "https://www.instagram.com/oliveleafindore?stkn=MXduZGk2ZzU3emZjdw==",
    instagramUsername: "@oliveleafindore",
    instagramSubtext: "Follow for Reels, Menu & Offers",

    // 4. Contact & Location Details
    phoneNumber: "9993896969",
    phoneButtonText: "Call / Reservation: 9993896969",
    address: "Shop 9, 10 Ground Floor, Skye Corporate Park, Scheme No. 78, Vijay Nagar, Indore",

    // 5. Footer Message
    footerThanks: "Thank you for dining at Olive Leaf! ✨",
    footerCity: "Crafted with care in Indore",

    // 6. Hosted Landing Page URL (Is link ka QR code banta hai)
    landingPageUrl: "https://namangarg-06.github.io/oliveleaf/"
};

// Expose globally for both browser and node/tools if needed
if (typeof module !== 'undefined' && module.exports) {
    module.exports = RESTAURANT_CONFIG;
}
