import React from 'react';

const LangBadge = ({ code, colorClass }) => (
    <div className={`w-10 shrink-0 flex justify-center items-center rounded py-1 px-1.5 border ${colorClass}`}>
        <span className="text-[0.65rem] font-bold tracking-wider uppercase">{code}</span>
    </div>
);

export default LangBadge;
