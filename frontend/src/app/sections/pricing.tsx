"use client";

import { motion } from "framer-motion";

export default function Pricing({ openModal }: { openModal: () => void }) {
  return (
    <div className="relative min-h-screen w-full overflow-hidden">
      <div className="relative z-10 mx-auto max-w-7xl px-6 py-24 sm:py-32 lg:px-8">
        <div className="mx-auto max-w-4xl text-center">
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="text-base font-semibold leading-7 text-purple-600 font-oddlini"
          >
            Pricing
          </motion.p>
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="mt-2 text-4xl font-oddlini sm:text-7xl"
          >
            Simple pricing for everyone.
          </motion.h2>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="mt-6 text-lg leading-8 text-gray-600 font-hanken"
          >
            Choose an <span className="font-medium">affordable plan</span>{" "}
            that's packed with the best features for engaging your audience,
            creating customer loyalty, and driving sales.
          </motion.p>
        </div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
          className="mt-6 flex items-center justify-center"
        >
          <div className="rounded-full border border-purple-600/10 bg-purple-50/50 px-3 py-1">
            <p className="text-sm font-medium text-purple-600 font-hanken">
              ✨ 14 day free trial
            </p>
          </div>
        </motion.div>

        <div className="mt-10 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-2">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.5 }}
            className="rounded-2xl border border-gray-200 bg-white p-8 shadow-sm"
          >
            <h3 className="text-lg font-semibold text-gray-900 font-oddlini">
              Basic
            </h3>
            <p className="mt-2 text-base text-gray-500 font-hanken">
              A basic plan for startups and individual users
            </p>
            <p className="mt-6 font-oddlini">
              <span className="text-4xl font-bold tracking-tight text-gray-900">
                $0.99
              </span>
              <span className="text-sm font-semibold text-gray-500">
                {" "}
                / month
              </span>
            </p>
            <button onClick={openModal} className="mt-6 w-full font-hanken rounded-lg bg-white px-3 py-2 text-center text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50">
              Subscribe
            </button>
            <ul className="mt-8 space-y-4 text-sm font-hanken">
              <li className="flex items-center gap-2">
                <svg
                  className="h-5 w-5 flex-none text-purple-600"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z"
                    clipRule="evenodd"
                  />
                </svg>
                AI-powered analytics
              </li>
              <li className="flex items-center gap-2">
                <svg
                  className="h-5 w-5 flex-none text-purple-600"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z"
                    clipRule="evenodd"
                  />
                </svg>
                Basic support
              </li>
              <li className="flex items-center gap-2">
                <svg
                  className="h-5 w-5 flex-none text-purple-600"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z"
                    clipRule="evenodd"
                  />
                </svg>
                5 projects limit
              </li>
            </ul>
          </motion.div>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.6 }}
            className="rounded-2xl border border-purple-600 bg-white p-8 shadow-sm ring-1 ring-purple-600"
          >
            <h3 className="text-lg font-semibold text-gray-900 font-oddlini">
              Premium
            </h3>
            <p className="mt-2 text-base text-gray-500 font-hanken">
              A premium plan for growing businesses
            </p>
            <p className="mt-6 font-oddlini">
              <span className="text-4xl font-bold tracking-tight text-gray-900">
                $1.99
              </span>
              <span className="text-sm font-semibold text-gray-500">
                {" "}
                / month
              </span>
            </p>
            <button onClick={openModal} className="mt-6 w-full font-hanken rounded-lg bg-purple-600 px-3 py-2 text-center text-sm font-semibold text-white shadow-sm hover:bg-purple-500">
              Subscribe
            </button>
            <ul className="mt-8 space-y-4 text-sm font-hanken">
              <li className="flex items-center gap-2">
                <svg
                  className="h-5 w-5 flex-none text-purple-600"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z"
                    clipRule="evenodd"
                  />
                </svg>
                Advanced AI insights
              </li>
              <li className="flex items-center gap-2">
                <svg
                  className="h-5 w-5 flex-none text-purple-600"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z"
                    clipRule="evenodd"
                  />
                </svg>
                Priority support
              </li>
              <li className="flex items-center gap-2">
                <svg
                  className="h-5 w-5 flex-none text-purple-600"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z"
                    clipRule="evenodd"
                  />
                </svg>
                Unlimited projects
              </li>
            </ul>
          </motion.div>
        </div>
      </div>
    </div>
  );
}
