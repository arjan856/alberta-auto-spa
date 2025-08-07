# Alberta Advantage Auto Spa Website

This website has been converted from a single-page application to a multi-page structure for better organization and user experience.

## File Structure


```
├── index.html              # Main homepage with services and testimonials
├── about.html              # About us page with team and company info
├── booking.html            # Dedicated booking form page
├── gallery.html            # Portfolio gallery with before/after photos
├── css/
│   └── style.css          # Shared CSS styles for all pages
├── js/
│   └── main.js            # Shared JavaScript functionality
├── images/                # All website images
│   ├── car1.jpg           # Hero background image
│   ├── car2.jpg           # Services background image
│   ├── car3.jpg           # Contact background image
│   └── ...                # Additional gallery images
└── Alberta_autospa_original.html  # Original single-page backup
```

## Pages Overview

### index.html (Homepage)
- Hero section with call-to-action
- Service packages display
- Customer testimonials
- Links to other pages

### about.html
- Company story and mission
- Team member profiles
- Core values and process
- Credentials and certifications
- Location and hours information

### booking.html
- Comprehensive booking form
- Service selection options
- Add-on services
- Contact information
- Form validation

### gallery.html
- Portfolio of completed work
- Before and after comparisons
- High-resolution images
- Service categories

## Key Features

- **Responsive Design**: Works on all devices
- **SEO Optimized**: Each page has unique titles and meta descriptions
- **Fast Loading**: Separated CSS and JavaScript for better performance
- **User Friendly**: Clear navigation and logical page flow
- **Professional**: Clean, modern design that builds trust

## Image Requirements

To complete the website, add these images to the `images/` folder:

### Required Images:
- `car1.jpg` - Hero background (1920x1080 recommended)
- `car2.jpg` - Services background (1920x1080 recommended)
- `car3.jpg` - Contact background (1920x1080 recommended)
- `car4.jpg` - `car6.jpg` - Gallery images (800x600 recommended)
- `customer1.jpg` - `customer3.jpg` - Customer photos (300x300 recommended)
- `owner-photo.jpg` - Owner photo for about page (400x400 recommended)
- `team-member2.jpg`, `team-member3.jpg` - Staff photos (400x400 recommended)
- `shop-exterior.jpg` - Business exterior photo (800x600 recommended)

### Optional Gallery Images:
- `truck1.jpg`, `suv1.jpg` - Additional vehicle types
- `detail1.jpg`, `detail2.jpg` - Close-up detail work
- `interior1.jpg`, `interior2.jpg` - Interior work
- `before1.jpg`, `after1.jpg` - Before/after exterior
- `before2.jpg`, `after2.jpg` - Before/after interior

## Form Setup

The booking form is configured to use FormSubmit.co. To activate:

1. Update the form action URL in `booking.html` (line 38)
2. Replace `albertautospa@gmail.com` with your actual email
3. Update the redirect URL (line 40) to your domain

## Social Media Links

Update the social media links in the footer sections of all pages:
- Facebook: Line varies by page
- Instagram: Line varies by page  
- TikTok: Line varies by page

## Browser Compatibility

- Chrome 60+
- Firefox 55+
- Safari 11+
- Edge 79+
- Internet Explorer is not supported

## Performance

- Optimized CSS with variables for consistent theming
- Compressed images recommended for faster loading
- Minimal JavaScript for essential functionality only
- Uses CDN for Font Awesome and Google Fonts

## Maintenance

- All styles are in `css/style.css`
- All JavaScript is in `js/main.js`
- Update contact information in all footer sections when needed
- Test forms regularly to ensure proper functionality

