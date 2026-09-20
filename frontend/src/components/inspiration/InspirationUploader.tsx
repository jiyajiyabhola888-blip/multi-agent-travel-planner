import React, { useState } from 'react';
import { Upload, Sparkles, Image as ImageIcon, MapPin, CheckCircle2, ArrowRight } from 'lucide-react';

interface InspirationUploaderProps {
  onAddExtractedPlace: (dest: string) => void;
  onBack?: () => void;
}

export const InspirationUploader: React.FC<InspirationUploaderProps> = ({ onAddExtractedPlace, onBack }) => {
  const [caption, setCaption] = useState<string>('');
  const [analyzing, setAnalyzing] = useState<boolean>(false);
  const [result, setResult] = useState<any>(null);

  const handleSimulatedUpload = (sampleDest: string, samplePoi: string, sampleVibe: string) => {
    setAnalyzing(true);
    setTimeout(() => {
      setAnalyzing(false);
      setResult({
        extracted_destination: sampleDest,
        detected_attraction: samplePoi,
        aesthetic_style: sampleVibe,
        confidence_score: 0.96,
        suggested_actions: [
          'Add directly to your upcoming itinerary',
          'Find similar panoramic viewpoints nearby',
          'Connect with verified local photography guide'
        ]
      });
    }, 800);
  };

  return (
    <div className="max-w-3xl mx-auto my-8 px-4 sm:px-6 space-y-6">
      <div className="card-clean p-6 sm:p-8 bg-white border border-slate-100 shadow-soft">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <span className="badge-pink text-xs px-2.5 py-1">Multimodal Vision AI</span>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-navy-900 mt-2">
              Screenshot & Photo Inspiration Import
            </h1>
            <p className="text-sm text-slate-500 mt-1">
              Upload an Instagram travel reel screenshot or travel photo. Our AI extracts the exact landmark and coordinates.
            </p>
          </div>
          {onBack && (
            <button onClick={onBack} className="btn-secondary text-xs py-2.5 px-4 self-start sm:self-auto">
              Back
            </button>
          )}
        </div>

        {/* Upload Dropzone */}
        <div className="mt-6 border-2 border-dashed border-slate-200 hover:border-brand-500 rounded-3xl p-8 text-center transition-colors bg-surface-50 cursor-pointer space-y-4">
          <div className="w-14 h-14 rounded-2xl bg-brand-50 text-brand-600 mx-auto flex items-center justify-center">
            <Upload className="w-6 h-6" />
          </div>
          <div>
            <h4 className="font-bold text-sm text-navy-900">Drag and drop your travel screenshot or photo</h4>
            <p className="text-xs text-slate-400 mt-1">PNG, JPG, WebP supported (Max 10MB)</p>
          </div>

          <div className="flex items-center justify-center gap-2 pt-2 flex-wrap">
            <span className="text-xs text-slate-400">Or try sample inspiration:</span>
            <button
              onClick={() => handleSimulatedUpload("Paris, France", "Eiffel Tower & Champ de Mars", "Romantic & Architectural")}
              className="text-xs badge-blue cursor-pointer hover:bg-brand-100"
            >
              📸 Paris Eiffel Tower
            </button>
            <button
              onClick={() => handleSimulatedUpload("Udaipur, Rajasthan", "Lake Pichola & City Palace", "Romantic Heritage Lake")}
              className="text-xs badge-pink cursor-pointer hover:bg-blush-100"
            >
              📸 Udaipur Palace Lake
            </button>
            <button
              onClick={() => handleSimulatedUpload("Interlaken, Switzerland", "Jungfraujoch Top of Europe", "Alpine Snow Peaks")}
              className="text-xs badge-blue cursor-pointer hover:bg-brand-100"
            >
              📸 Swiss Alps
            </button>
          </div>
        </div>

        {/* Analyzing Spinner */}
        {analyzing && (
          <div className="py-8 text-center space-y-2 animate-fadeIn">
            <Sparkles className="w-8 h-8 text-brand-600 animate-spin mx-auto" />
            <p className="text-xs text-slate-600 font-semibold">Analyzing image landmarks with Vision AI...</p>
          </div>
        )}

        {/* Vision AI Result Card */}
        {result && !analyzing && (
          <div className="mt-6 p-6 rounded-2xl bg-gradient-to-br from-brand-50 to-blush-50 border border-brand-200 animate-fadeIn space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-brand-100">
              <div className="flex items-center gap-2">
                <CheckCircle2 className="w-5 h-5 text-emerald-600" />
                <h4 className="font-bold text-sm text-navy-900">Landmark Successfully Detected!</h4>
              </div>
              <span className="text-[11px] font-bold text-brand-700">★ {Math.round(result.confidence_score * 100)}% Confidence</span>
            </div>

            <div className="space-y-1.5 text-xs">
              <p><strong>Identified Location:</strong> {result.extracted_destination}</p>
              <p><strong>Attraction:</strong> {result.detected_attraction}</p>
              <p><strong>Vibe / Aesthetic:</strong> {result.aesthetic_style}</p>
            </div>

            <div className="pt-2">
              <button
                onClick={() => onAddExtractedPlace(result.extracted_destination)}
                className="btn-primary w-full text-xs py-3"
              >
                <span>Plan Trip to {result.extracted_destination}</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
