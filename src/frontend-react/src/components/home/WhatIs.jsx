import Image from 'next/image';
import styles from './WhatIs.module.css';
import Link from 'next/link';

export default function WhatIs() {
    return (
        <section className={styles.section}>
            <h2 className={styles.title}>Ready for Bird Watching App!</h2>
            <div className={styles.underline}></div>

            <div className={styles.content}>
                <div className={styles.textContent}>
                    <h3 className={styles.subtitle}>Discover the birds of Yanachaga Chemillen National Park with Bird Watching App!</h3>

                    <p>
                        Welcome to <strong>Yanachaga Chemillén National Park</strong>, part of the ancestral lands of the Ashaninka and Yanesha Indigenous communities in Peru.
                        This richly biodiverse region is home to over 500 bird species, many of which are <em>endemic</em> — found nowhere else on Earth.
                    </p>

                    <p>
                        Not sure which bird you are hearing or seeing? Just record its call. Our app uses an <strong>AI-powered acoustic model</strong> to identify bird species
                        with remarkable accuracy. It is as simple as point, record, and discover.
                    </p>

                    <p>
                        Once your bird is identified, dive deeper: explore its habitat and previous sightings through our <strong>interactive maps</strong>, which include
                        environmental data such as deforestation and other habitat conditions.
                    </p>

                    <p>
                        Have more questions? Our built-in <strong>chatbot</strong> is ready to assist. Ask anything about the bird species you have discovered.
                    </p>

                    <p>
                        Whether you are new to birdwatching or a seasoned expert, the Bird Watching App is your companion in exploring the incredible avian life of
                        Yanachaga Chemillén. It is more than just an app: it is a journey into the heart of Peru’s natural heritage.
                    </p>

                    <div className={styles.features}>
                        <h4>Key Features:</h4>
                        <ul>
                            <li>Instantly recognize birds by their calls using advanced AI-powered sound analysis.</li>
                            <li>Explore where birds live and have been previously recorded, along with habitat conditions such as land cover, biodiversity hotspots, and deforestation.</li>                            
                            <li>Ask questions and get answers through our intelligent chatbot trained on bird knowledge.</li> 
                            <li>Browse and listen to curated audio recordings of bird species from the national park.</li>                          
                            <li>Perfect for bird enthusiasts, advanced bird watchers, and anyone looking to explore the world of birds</li>
                        </ul>
                    </div>
                 
                </div>

                <div className={styles.imageBlock}>
                    {/* This div is just for the image */}
                    <div style={{ position: 'relative', width: '100%', height: '360px', marginTop: '40px' }}>
                        <Image
                            src="/assets/localbird.png"
                            alt="Local bird"
                            fill
                            sizes="(max-width: 768px) 100vw, 400px"
                            style={{ objectFit: 'cover' }}
                            priority
                        />
                    </div>

                    {/* Caption now outside of the image box */}
                    <p style={{
                        fontSize: '14px',
                        color: '#666',
                        textAlign: 'right',
                        marginTop: '8px'
                    }}>
                        Versicolored Barbet, Photography by Joao Quental
                    </p>
                </div>


            </div>
            <div style={{
                width: '100%',
                marginTop: '80px',
                textAlign: 'center',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center'
            }}>
                <h2 className={styles.title}>
                    Got a bird recording?<br></br> Identify it with our Bird Assistant.
                </h2>
                <p style={{
                    fontSize: '18px',
                    color: '#333',
                    fontWeight: '400',
                    fontFamily: "'Source Sans Pro', sans-serif",
                    lineHeight: '1.6',
                    maxWidth: '700px'
                    }}>
                    Upload your audio and let our AI-powered assistant reveal the species behind the sound—ready to answer your questions and help you explore more.
                </p>
                <Link href="/chat" style={{
                    backgroundColor: '#666',
                    color: 'white',
                    padding: '10px 20px',
                    borderRadius: '0px',
                    textDecoration: 'none',
                    display: 'inline-block',
                    marginTop: '30px'
                }}>
                    Access Bird Assistant
                </Link>
            </div>
        </section>
    );
}