import React from "react";
import { useAuth } from "@/contexts/AuthContext";
import HeroSection from "@/components/home/HeroSection";
import ServicesSection from "@/components/home/ServicesSection";
import CtaSection from "@/components/home/CtaSection";
import BenefitsSection from "@/components/home/BenefitsSection";

const HomePage = () => {
  const { user } = useAuth();

  return (
    <div>
      <HeroSection user={user} />
      <ServicesSection />
      <CtaSection user={user} />
      <BenefitsSection />
    </div>
  );
};

export default HomePage;
