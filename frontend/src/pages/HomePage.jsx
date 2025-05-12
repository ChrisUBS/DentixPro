
import React from "react";
import { getCurrentSession } from "@/lib/auth-service";
import HeroSection from "@/components/home/HeroSection";
import ServicesSection from "@/components/home/ServicesSection";
import CtaSection from "@/components/home/CtaSection";
import BenefitsSection from "@/components/home/BenefitsSection";

const HomePage = () => {
  const session = getCurrentSession();

  return (
    <div>
      <HeroSection session={session} />
      <ServicesSection />
      <CtaSection session={session} />
      <BenefitsSection />
    </div>
  );
};

export default HomePage;
