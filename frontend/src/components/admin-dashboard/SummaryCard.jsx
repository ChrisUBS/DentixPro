
import React from "react";
import { Card, CardContent } from "@/components/ui/card";

const SummaryCard = ({ title, value, icon, gradientFrom, gradientTo, borderColor, textColor, iconBgColor, iconColor }) => {
  return (
    <Card className={`bg-gradient-to-br ${gradientFrom} ${gradientTo} ${borderColor}`}>
      <CardContent className="p-6">
        <div className="flex items-center justify-between">
          <div>
            <p className={`text-sm font-medium ${textColor}`}>{title}</p>
            <h3 className={`text-3xl font-bold ${textColor}`}>{value}</h3>
          </div>
          <div className={`${iconBgColor} p-3 rounded-full`}>
            {React.cloneElement(icon, { className: `h-6 w-6 ${iconColor}` })}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default SummaryCard;
