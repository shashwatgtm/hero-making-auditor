// Production Hero Customer Discovery Actor
import { Actor } from 'apify';
import { CheerioCrawler, log } from 'crawlee';

await Actor.init();

try {
    const input = await Actor.getInput();
    log.info('Hero Customer Discovery Actor started');
    
    const {
        companyName,
        companyWebsite,
        maxResults = 50,
        searchDepth = 3,
        includeTestimonials = true,
        includeCaseStudies = true,
        includeReviews = true
    } = input || {};

    if (!companyName) {
        throw new Error('companyName is required');
    }

    log.info(`Analyzing customers for: ${companyName}`);
    
    // Real implementation - web scraping for actual customer data
    const discoveredCustomers = [];
    const searchUrls = [];
    
    // Build comprehensive search strategy
    if (companyWebsite) {
        const baseUrl = new URL(companyWebsite).origin;
        searchUrls.push(
            `${baseUrl}/customers`,
            `${baseUrl}/case-studies`,
            `${baseUrl}/testimonials`,
            `${baseUrl}/success-stories`
        );
    }
    
    // Google search for customer mentions
    const searchQueries = [
        `"${companyName}" customer case study`,
        `"${companyName}" client testimonial`,
        `"${companyName}" success story`,
        `site:${companyWebsite} customer`
    ];
    
    searchQueries.forEach(query => {
        searchUrls.push(`https://www.google.com/search?q=${encodeURIComponent(query)}&num=10`);
    });
    
    const crawler = new CheerioCrawler({
        maxRequestsPerCrawl: searchDepth * 10,
        maxConcurrency: 3,
        
        async requestHandler({ $, request }) {
            log.info(`Processing: ${request.url}`);
            
            const customers = [];
            
            // Extract customer names from various page elements
            const customerSections = $('[class*="customer"], [class*="client"], [class*="testimonial"], [class*="case-study"]');
            
            customerSections.each((i, element) => {
                const $element = $(element);
                const text = $element.text().trim();
                
                // Extract company names using regex
                const companyPattern = /\b([A-Z][a-zA-Z\s&.,-]{2,40}(?:\s(?:Inc|LLC|Corp|Company|Ltd))?)\b/g;
                let match;
                
                while ((match = companyPattern.exec(text)) !== null) {
                    const customerName = match[1].trim();
                    
                    if (customerName.length > 2 && 
                        customerName.length < 50 && 
                        !customerName.toLowerCase().includes(companyName.toLowerCase())) {
                        
                        customers.push({
                            name: customerName,
                            source: request.url,
                            context: text.substring(0, 200),
                            confidence: calculateConfidence(text, customerName),
                            discoveredAt: new Date().toISOString()
                        });
                    }
                }
            });
            
            if (customers.length > 0) {
                discoveredCustomers.push(...customers);
                log.info(`Found ${customers.length} customers on ${request.url}`);
            }
        }
    });
    
    await crawler.addRequests(searchUrls.map(url => ({ url })));
    await crawler.run();
    
    // Process and deduplicate results
    const uniqueCustomers = deduplicateCustomers(discoveredCustomers);
    const finalCustomers = uniqueCustomers
        .sort((a, b) => b.confidence - a.confidence)
        .slice(0, maxResults);
    
    const result = {
        companyName,
        companyWebsite,
        timestamp: new Date().toISOString(),
        customers: finalCustomers,
        summary: {
            totalCustomersFound: finalCustomers.length,
            averageConfidence: finalCustomers.length > 0 ? 
                (finalCustomers.reduce((sum, c) => sum + c.confidence, 0) / finalCustomers.length).toFixed(3) : 0,
            urlsProcessed: searchUrls.length
        },
        status: 'SUCCESS'
    };
    
    await Actor.pushData(result);
    log.info(`Discovery completed. Found ${finalCustomers.length} customers.`);
    
} catch (error) {
    log.error(`Actor failed: ${error.message}`);
    
    await Actor.pushData({
        companyName: input?.companyName || 'Unknown',
        timestamp: new Date().toISOString(),
        status: 'ERROR',
        error: error.message,
        customers: []
    });
    
    throw error;
}

function calculateConfidence(text, customerName) {
    let confidence = 0.5;
    
    const positiveKeywords = ['customer', 'client', 'testimonial', 'case study', 'success'];
    positiveKeywords.forEach(keyword => {
        if (text.toLowerCase().includes(keyword)) {
            confidence += 0.1;
        }
    });
    
    if (/\b(Inc|LLC|Corp|Company|Ltd)\b/.test(customerName)) {
        confidence += 0.1;
    }
    
    return Math.min(confidence, 0.99);
}

function deduplicateCustomers(customers) {
    const seen = new Map();
    return customers.filter(customer => {
        const key = customer.name.toLowerCase().trim();
        if (seen.has(key)) {
            return false;
        }
        seen.set(key, customer);
        return true;
    });
}

await Actor.exit();