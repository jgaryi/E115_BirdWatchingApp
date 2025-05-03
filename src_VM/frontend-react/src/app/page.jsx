import Hero from '@/components/home/Hero';
import About from '@/components/home/About';
import Bird_sounds from '@/components/home/Bird_sounds';
import Bird_maps from '@/components/home/Bird_maps';
import WhatIs from '@/components/home/WhatIs';

export default function Home() {
    return (
        <>
            <Hero />
            <WhatIs></WhatIs>
            <Bird_sounds />
            <Bird_maps />
            <About />
        </>
    )
}