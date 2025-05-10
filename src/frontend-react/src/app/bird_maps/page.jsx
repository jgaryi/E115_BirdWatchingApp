'use client';

import { useState, useEffect, use } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import DataService from "../../services/DataService";

// Import the styles
import styles from "./styles.module.css";

export default function bird_mapsPage({ searchParams }) {
    const params = use(searchParams);
    const bird_map_id = params.id;

    // Component States
    const [bird_maps, setbird_maps] = useState([]);
    const [hasActivebird_map, setHasActivebird_map] = useState(false);
    const [bird_map, setbird_map] = useState(null);

    const fetchbird_map = async (id) => {
        try {
            setbird_map(null);
            const response = await DataService.Getbird_map(id);
            setbird_map(response.data);
            console.log(bird_map);
        } catch (error) {
            console.error('Error fetching bird_map:', error);
            setbird_map(null);
        }
    };

    // Setup Component
    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await DataService.Getbird_maps(100);
                setbird_maps(response.data);
            } catch (error) {
                console.error('Error fetching bird_sounds:', error);
                setbird_maps([]); // Set empty array in case of error
            }
        };

        fetchData();
    }, []);
    useEffect(() => {
        if (bird_map_id) {
            fetchbird_map(bird_map_id);
            setHasActivebird_map(true);
        } else {
            setbird_map(null);
            setHasActivebird_map(false);
        }
    }, [bird_map_id]);

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
            {!hasActivebird_map && (
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

            {/* bird_map Grid */}
            {!hasActivebird_map && (
                <section className={styles.bird_mapSection}>
                    <div className={styles.grid}>
                        {bird_maps.map((bird_map) => (
                            <article key={bird_map.id} className={styles.card}>
                                <div className={styles.imageContainer}>
                                    <img
                                        src={`/assets/${bird_map.image}`}
                                        alt={bird_map.title}
                                        width={400}
                                        height={250}
                                        className={styles.image}
                                    />
                                    <span className={styles.category}>{bird_map.category}</span>
                                </div>

                                <div className={styles.content}>
                                    <div className={styles.meta}>
                                        <span className={styles.date}>{bird_map.date}</span>
                                        <span className={styles.readTime}>{bird_map.readTime}</span>
                                    </div>

                                    <h3 className={styles.title}>{bird_map.title}</h3>
                                    <p className={styles.excerpt}>{bird_map.excerpt}</p>

                                    <Link href={`/bird_maps?id=${bird_map.id}`} className={styles.readMore}>
                                        Discover More <span className={styles.arrow}>→</span>
                                    </Link>
                                </div>
                            </article>
                        ))}
                    </div>

                    {/* bird_map Subscription */}
                    <div className={styles.subscriptionBox}>
                        <h3>Stay Updated</h3>
                        <p>Subscribe to receive our bird_map featuring bird species in Yanachaga Chemillén National Park, along with their locations and habitat conditions, delivered straight to your inbox!</p>
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

            {/* bird_map Detail View */}
            {hasActivebird_map && bird_map && (
                <section className={styles.bird_mapDetail}>
                    <div className={styles.detailContainer}>
                        <Link href="/bird_maps" className={styles.backButton}>
                            ← Back to Interactive Maps
                        </Link>

                        <div className={styles.detailHeader}>
                            <span className={styles.detailCategory}>{bird_map.category}</span>
                            <div className={styles.detailMeta}>
                                <span className={styles.date}>{bird_map.date}</span>
                                <span className={styles.readTime}>{bird_map.readTime}</span>
                            </div>
                            <h1 className={styles.detailTitle}>{bird_map.title}</h1>
                        </div>

                        <div className={styles.detailImageContainer}>
                            {bird_map.html ? (
                                <iframe
                                    src={`/assets/${bird_map.html}`}
                                    title={bird_map.title}
                                    width="100%"
                                    height="400"
                                    style={{ border: '1px solid #ccc' }}
                                />
                                ) : (
                                <p style={{ padding: '1rem', color: '#666' }}>
                                    No interactive content available for this bird_map.
                                </p>
                            )}
                        </div>

                        <div className={styles.detailContent}>
                            <div dangerouslySetInnerHTML={{ __html: bird_map.detail }} />
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