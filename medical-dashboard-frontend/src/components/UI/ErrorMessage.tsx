import React from 'react';
import { AlertTriangle, X } from 'lucide-react';

interface ErrorMessageProps {
  title?: string;
  message: string;
  onRetry?: () => void;
  onDismiss?: () => void;
}

export const ErrorMessage: React.FC<ErrorMessageProps> = ({
  title = 'Erreur',
  message,
  onRetry,
  onDismiss,
}) => {
  return (
    <div className="bg-red-50 border border-red-200 rounded-lg p-4 relative">
      {onDismiss && (
        <button
          onClick={onDismiss}
          className="absolute top-2 right-2 text-red-400 hover:text-red-600"
        >
          <X size={18} />
        </button>
      )}
      <div className="flex items-start">
        <AlertTriangle className="text-red-500 mr-3 mt-0.5 flex-shrink-0" size={20} />
        <div>
          <h3 className="text-red-800 font-semibold">{title}</h3>
          <p className="text-red-700 text-sm mt-1">{message}</p>
          {onRetry && (
            <button
              onClick={onRetry}
              className="mt-3 px-4 py-2 bg-red-100 text-red-700 rounded-md text-sm font-medium hover:bg-red-200 transition-colors"
            >
              Réessayer
            </button>
          )}
        </div>
      </div>
    </div>
  );
};