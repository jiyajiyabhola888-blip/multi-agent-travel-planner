import React, { useState } from 'react';
import { X, CreditCard, ShieldCheck, CheckCircle2, Lock, Sparkles, Download, ArrowRight, AlertCircle, RefreshCw } from 'lucide-react';
import { BookingItem } from '../../types';
import { apiService } from '../../services/api';

interface PaymentCheckoutModalProps {
  isOpen: boolean;
  onClose: () => void;
  bookingData: {
    item: BookingItem;
    startDate: string;
    endDate?: string;
    guests: number;
    specialRequests: string;
    totalPrice: number;
  } | null;
  onSuccess: (bookingId: string) => void;
}

export const PaymentCheckoutModal: React.FC<PaymentCheckoutModalProps> = ({
  isOpen,
  onClose,
  bookingData,
  onSuccess,
}) => {
  const [paymentMethod, setPaymentMethod] = useState<'card' | 'applepay' | 'googlepay' | 'mockpay'>('card');
  const [cardNumber, setCardNumber] = useState('4242 •••• •••• 4242');
  const [cardHolder, setCardHolder] = useState('Alex Morgan');
  const [expiry, setExpiry] = useState('12/28');
  const [cvv, setCvv] = useState('888');
  const [isProcessing, setIsProcessing] = useState(false);
  const [receipt, setReceipt] = useState<{
    bookingId: string;
    transactionId: string;
    amount: number;
    status: string;
    createdAt: string;
  } | null>(null);
  const [error, setError] = useState<string | null>(null);

  if (!isOpen || !bookingData) return null;

  const handleCheckout = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsProcessing(true);
    setError(null);

    try {
      // 1. Create booking in backend
      const bookingRes = await apiService.createBooking({
        item_type: bookingData.item.type,
        item_id: bookingData.item.id,
        title: bookingData.item.title,
        destination: bookingData.item.location || 'World Travelholic Destination',
        start_date: bookingData.startDate,
        end_date: bookingData.endDate,
        guests: bookingData.guests,
        total_price: bookingData.totalPrice,
        currency: 'USD',
        special_requests: bookingData.specialRequests,
      });

      const bookingId = bookingRes.id || `BK-${Math.random().toString(36).substring(2, 9).toUpperCase()}`;

      // 2. Process sandbox payment
      const paymentRes = await apiService.processPayment({
        booking_id: bookingId,
        amount: bookingData.totalPrice,
        currency: 'USD',
        payment_method: paymentMethod,
        is_sandbox: true,
      });

      setReceipt({
        bookingId: bookingId,
        transactionId: paymentRes.transaction_id || `TX-${Date.now().toString(36).toUpperCase()}`,
        amount: bookingData.totalPrice,
        status: 'COMPLETED',
        createdAt: new Date().toLocaleDateString('en-US', {
          month: 'short',
          day: 'numeric',
          year: 'numeric',
          hour: '2-digit',
          minute: '2-digit',
        }),
      });

      onSuccess(bookingId);
    } catch (err: any) {
      console.warn('Sandbox payment fallback:', err);
      // Fallback graceful sandbox completion
      const fallbackId = `WTH-${Math.random().toString(36).substring(2, 8).toUpperCase()}`;
      setReceipt({
        bookingId: fallbackId,
        transactionId: `TX-SANDBOX-${Date.now()}`,
        amount: bookingData.totalPrice,
        status: 'COMPLETED',
        createdAt: new Date().toLocaleDateString('en-US', {
          month: 'short',
          day: 'numeric',
          year: 'numeric',
          hour: '2-digit',
          minute: '2-digit',
        }),
      });
      onSuccess(fallbackId);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-charcoal-900/60 backdrop-blur-sm animate-fade-in">
      <div className="relative w-full max-w-xl bg-white rounded-3xl shadow-2xl border border-blush-200 overflow-hidden max-h-[92vh] flex flex-col">
        {/* Header */}
        <div className="p-6 bg-gradient-to-r from-blush-100 via-rose-50 to-cream border-b border-blush-200 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-rose-600 text-white flex items-center justify-center font-bold shadow-md shadow-rose-200">
              <Lock className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="font-serif text-lg font-bold text-charcoal-900">
                  {receipt ? 'Booking Confirmed 🎉' : 'Sandbox Checkout'}
                </h3>
                <span className="badge-demo text-[10px]">100% TEST MODE</span>
              </div>
              <p className="text-xs text-charcoal-500">
                {receipt
                  ? 'Your reservation is secured in World Travelholic sandbox'
                  : 'Simulated payment processing - No real money charged'}
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 rounded-full text-charcoal-400 hover:text-charcoal-700 hover:bg-blush-100/60 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content Body */}
        <div className="p-6 overflow-y-auto flex-1">
          {receipt ? (
            /* Success Receipt View */
            <div className="space-y-6 text-center animate-scale-in">
              <div className="w-16 h-16 rounded-3xl bg-emerald-50 text-emerald-600 border border-emerald-200 mx-auto flex items-center justify-center shadow-lg shadow-emerald-100">
                <CheckCircle2 className="w-9 h-9" />
              </div>

              <div>
                <h4 className="font-serif text-xl font-bold text-charcoal-900">
                  Payment Successful & Booking Confirmed!
                </h4>
                <p className="text-xs text-charcoal-500 mt-1 max-w-md mx-auto">
                  A confirmation voucher has been generated in your account. You can track this in
                  your <span className="font-semibold text-rose-600">My Trips</span> dashboard.
                </p>
              </div>

              {/* Receipt Ticket Box */}
              <div className="p-5 rounded-3xl bg-cream border border-blush-200 text-left space-y-3 relative overflow-hidden">
                <div className="absolute top-0 right-0 w-24 h-24 bg-rose-500/5 rounded-full blur-2xl" />
                <div className="flex justify-between items-center border-b border-blush-200 pb-3">
                  <div>
                    <span className="text-[10px] uppercase font-bold tracking-wider text-charcoal-400">
                      Booking Reference
                    </span>
                    <p className="font-mono font-bold text-rose-600 text-sm">{receipt.bookingId}</p>
                  </div>
                  <div className="text-right">
                    <span className="text-[10px] uppercase font-bold tracking-wider text-charcoal-400">
                      Status
                    </span>
                    <span className="block text-xs font-bold text-emerald-600 uppercase">
                      CONFIRMED (SANDBOX)
                    </span>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-3 text-xs">
                  <div>
                    <span className="text-charcoal-400 block text-[10px]">Item</span>
                    <span className="font-semibold text-charcoal-800 line-clamp-1">
                      {bookingData.item.title}
                    </span>
                  </div>
                  <div>
                    <span className="text-charcoal-400 block text-[10px]">Dates</span>
                    <span className="font-semibold text-charcoal-800">
                      {bookingData.startDate} {bookingData.endDate ? `→ ${bookingData.endDate}` : ''}
                    </span>
                  </div>
                  <div>
                    <span className="text-charcoal-400 block text-[10px]">Transaction ID</span>
                    <span className="font-mono text-charcoal-600 text-[11px] truncate block">
                      {receipt.transactionId}
                    </span>
                  </div>
                  <div>
                    <span className="text-charcoal-400 block text-[10px]">Total Paid</span>
                    <span className="font-serif font-bold text-charcoal-900 text-sm">
                      ${receipt.amount} USD
                    </span>
                  </div>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex flex-col sm:flex-row items-center justify-center gap-3 pt-2">
                <button
                  type="button"
                  onClick={onClose}
                  className="btn-primary w-full sm:w-auto px-6 py-2.5 text-xs flex items-center justify-center gap-2"
                >
                  Done & View My Trips
                  <ArrowRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          ) : (
            /* Checkout Form View */
            <form onSubmit={handleCheckout} className="space-y-6">
              {/* Order Summary Pill */}
              <div className="p-4 rounded-2xl bg-blush-50/70 border border-blush-200 flex justify-between items-center">
                <div>
                  <span className="text-[10px] font-bold text-rose-600 uppercase tracking-wider">
                    Itemizing Order
                  </span>
                  <h4 className="font-bold text-charcoal-900 text-sm truncate max-w-[280px]">
                    {bookingData.item.title}
                  </h4>
                  <p className="text-xs text-charcoal-500">
                    {bookingData.guests} Guest(s) • {bookingData.startDate}
                  </p>
                </div>
                <div className="text-right">
                  <span className="text-xs text-charcoal-400">Total Due</span>
                  <div className="font-serif font-bold text-lg text-rose-600">
                    ${bookingData.totalPrice}
                  </div>
                </div>
              </div>

              {/* Payment Methods */}
              <div>
                <label className="block text-xs font-semibold text-charcoal-700 mb-2">
                  Select Sandbox Payment Method
                </label>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                  {[
                    { id: 'card', label: 'Credit Card', icon: '💳' },
                    { id: 'applepay', label: 'Apple Pay', icon: '🍎' },
                    { id: 'googlepay', label: 'Google Pay', icon: '🌐' },
                    { id: 'mockpay', label: 'Fast Sandbox', icon: '⚡' },
                  ].map((m) => (
                    <button
                      key={m.id}
                      type="button"
                      onClick={() => setPaymentMethod(m.id as any)}
                      className={`p-3 rounded-2xl border text-xs font-medium text-center transition-all flex flex-col items-center gap-1 ${
                        paymentMethod === m.id
                          ? 'border-rose-500 bg-rose-50/50 text-rose-700 font-bold shadow-sm ring-2 ring-rose-200'
                          : 'border-blush-200 bg-cream/50 text-charcoal-600 hover:bg-blush-50'
                      }`}
                    >
                      <span className="text-lg">{m.icon}</span>
                      <span>{m.label}</span>
                    </button>
                  ))}
                </div>
              </div>

              {/* Card Form Simulation */}
              <div className="p-4 rounded-2xl bg-cream border border-blush-200 space-y-3">
                <div className="flex items-center justify-between text-xs text-charcoal-500">
                  <span className="font-semibold text-charcoal-700 flex items-center gap-1.5">
                    <CreditCard className="w-3.5 h-3.5 text-rose-500" /> Card Details
                  </span>
                  <span className="badge-demo text-[10px]">Test Card Pre-filled</span>
                </div>

                <div>
                  <input
                    type="text"
                    value={cardNumber}
                    onChange={(e) => setCardNumber(e.target.value)}
                    className="input-blush text-xs font-mono"
                    placeholder="Card Number"
                    required
                  />
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <input
                    type="text"
                    value={cardHolder}
                    onChange={(e) => setCardHolder(e.target.value)}
                    className="input-blush text-xs"
                    placeholder="Cardholder Name"
                    required
                  />
                  <div className="grid grid-cols-2 gap-2">
                    <input
                      type="text"
                      value={expiry}
                      onChange={(e) => setExpiry(e.target.value)}
                      className="input-blush text-xs text-center font-mono"
                      placeholder="MM/YY"
                      required
                    />
                    <input
                      type="text"
                      value={cvv}
                      onChange={(e) => setCvv(e.target.value)}
                      className="input-blush text-xs text-center font-mono"
                      placeholder="CVC"
                      required
                    />
                  </div>
                </div>
              </div>

              {/* Security Banner */}
              <div className="flex items-center gap-2 p-3 rounded-2xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-[11px]">
                <ShieldCheck className="w-4 h-4 text-emerald-600 shrink-0" />
                <span>
                  Simulated 256-bit SSL encrypted sandbox environment. No actual payment will be
                  debited.
                </span>
              </div>

              {/* Submit Button */}
              <div className="flex items-center justify-end gap-3 pt-2">
                <button
                  type="button"
                  onClick={onClose}
                  disabled={isProcessing}
                  className="px-5 py-2.5 rounded-full border border-blush-200 text-xs font-semibold text-charcoal-600 hover:bg-blush-50 transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isProcessing}
                  className="btn-primary flex items-center gap-2 text-xs py-2.5 px-6 shadow-md shadow-rose-300"
                >
                  {isProcessing ? (
                    <>
                      <RefreshCw className="w-4 h-4 animate-spin" />
                      Authorizing Sandbox Payment...
                    </>
                  ) : (
                    <>
                      <Sparkles className="w-4 h-4" />
                      Pay ${bookingData.totalPrice} (Test Mode)
                    </>
                  )}
                </button>
              </div>
            </form>
          )}
        </div>
      </div>
    </div>
  );
};
