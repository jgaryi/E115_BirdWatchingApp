'use client';

import { useState, useEffect, use } from 'react';
import Image from 'next/image';
import Link from 'next/link';
//import DataService from "../../services/MockDataService"; // Mock
import DataService from "../../services/DataService";

// Import the styles
import styles from "./styles.module.css";


export default function NewslettersPage({ searchParams }) {
    const params = use(searchParams);
    const newsletter_id = params.id;

    // Component States
    const [newsletters, setNewsletters] = useState([]);
    const [hasActiveNewsletter, setHasActiveNewsletter] = useState(false);
    const [newsletter, setNewsletter] = useState(null);

    const fetchNewsletter = async (id) => {
        try {
            setNewsletter(null);
            const response = await DataService.GetNewsletter(id);
            setNewsletter(response.data);
            console.log(newsletter);
        } catch (error) {
            console.error('Error fetching newsletter:', error);
            setNewsletter(null);
        }
    };

    // Setup Component
    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await DataService.GetNewsletters(100);
                setNewsletters(response.data);
            } catch (error) {
                console.error('Error fetching podcasts:', error);
                setNewsletters([]); // Set empty array in case of error
            }
        };

        fetchData();
    }, []);
    useEffect(() => {
        if (newsletter_id) {
            fetchNewsletter(newsletter_id);
            setHasActiveNewsletter(true);
        } else {
            setNewsletter(null);
            setHasActiveNewsletter(false);
        }
    }, [newsletter_id]);

    return (
        <div className={styles.container}>
            {/* Hero Section */}
            <section className={styles.hero}>
                <div className={styles.heroContent}>
                    <h1>Interactive Maps</h1>
                    <p>Journey through our collection of maps and discover the world of birds within Yanachaga Chemillén National Park.</p>
                </div>
            </section>

            {/* About Section */}
            {!hasActiveNewsletter && (
                <section className={styles.about}>
                    <div className={styles.aboutContent}>
                        <h2>About Interactive Maps</h2>
                        <p>
                        Welcome to the Bird Watching App’s Interactive Maps — your gateway to exploring the rich biodiversity of Yanachaga Chemillén National Park!
                        These dynamic maps provide an in-depth look at bird habitats, species sightings, and changing environmental conditions, powered by expert field data and remote sensing technologies.
                        By integrating satellite imagery and ecological insights, our maps offer a powerful tool for understanding how birds interact with their environment — from forest cover to areas impacted by deforestation.
                        </p>
                    </div>
                </section>
            )}

            {/* Newsletter Grid */}
            {!hasActiveNewsletter && (
                <section className={styles.newsletterSection}>
                    <div className={styles.grid}>
                        {newsletters.map((newsletter) => (
                            <article key={newsletter.id} className={styles.card}>
                                <div className={styles.imageContainer}>
                                    <img
                                        src={DataService.GetNewsletterImage(newsletter.image)}
                                        alt={newsletter.title}
                                        width={400}
                                        height={250}
                                        className={styles.image}
                                    />
                                    <span className={styles.category}>{newsletter.category}</span>
                                </div>

                                <div className={styles.content}>
                                    <div className={styles.meta}>
                                        <span className={styles.date}>{newsletter.date}</span>
                                        <span className={styles.readTime}>{newsletter.readTime}</span>
                                    </div>

                                    <h3 className={styles.title}>{newsletter.title}</h3>
                                    <p className={styles.excerpt}>{newsletter.excerpt}</p>

                                    <Link href={`/newsletters?id=${newsletter.id}`} className={styles.readMore}>
                                        Discover More <span className={styles.arrow}>→</span>
                                    </Link>
                                </div>
                            </article>
                        ))}
                    </div>

                    {/* Newsletter Subscription */}
                    <div className={styles.subscriptionBox}>
                        <h3>Stay Updated</h3>
                        <p>Subscribe to receive our newsletter featuring bird species in Yanachaga Chemillén National Park, along with their locations and habitat conditions, delivered straight to your inbox!</p>
                        <form className={styles.subscriptionForm}>
                            <input
                                type="email"
                                placeholder="Enter your email"
                                className={styles.emailInput}
                            />
                            <button type="submit" className={styles.subscribeButton}>
                                Subscribe
                            </button>
                        </form>
                    </div>
                </section>
            )}

            {/* Newsletter Detail View */}
            {hasActiveNewsletter && newsletter && (
                <section className={styles.newsletterDetail}>
                    <div className={styles.detailContainer}>
                        <Link href="/newsletters" className={styles.backButton}>
                            ← Back to Interactive Maps
                        </Link>

                        <div className={styles.detailHeader}>
                            <span className={styles.detailCategory}>{newsletter.category}</span>
                            <div className={styles.detailMeta}>
                                <span className={styles.date}>{newsletter.date}</span>
                                <span className={styles.readTime}>{newsletter.readTime}</span>
                            </div>
                            <h1 className={styles.detailTitle}>{newsletter.title}</h1>
                        </div>

                        <div className={styles.detailImageContainer}>
                            {newsletter.html ? (
                                <iframe
                                    src={`/assets/${newsletter.html}`}
                                    title={newsletter.title}
                                    width="100%"
                                    height="400"
                                    style={{ border: '1px solid #ccc' }}
                                />
                                ) : (
                                <p style={{ padding: '1rem', color: '#666' }}>
                                    No interactive content available for this newsletter.
                                </p>
                            )}
                        </div>

                        <div className={styles.detailContent}>
                            <div dangerouslySetInnerHTML={{ __html: newsletter.detail }} />
                        </div>

                        <div className={styles.shareSection}>
                            <h3>Share this map</h3>
                            <div className={styles.shareButtons}>
                                <button className={styles.shareButton}>Twitter</button>
                                <button className={styles.shareButton}>Facebook</button>
                                <button className={styles.shareButton}>LinkedIn</button>
                            </div>
                        </div>
                    </div>
                </section>
            )}
        </div>
    );
}