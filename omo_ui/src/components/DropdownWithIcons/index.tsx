import { Fragment } from 'react'
import { Menu, Transition } from '@headlessui/react'
import {
  ChevronDownIcon,
  TrashIcon,
  DocumentPlusIcon
} from '@heroicons/react/24/outline';
import { classNames } from '@/utils/common';
import Link from 'next/link';

export default function DropdownWithIcons() {
  const lightStylesMenu = 'bg-white text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50'
  const darkStylesMenu = 'dark:bg-n-7 dark:hover:text-white dark:text-n-3 dark:hover:text-white dark:ring-n-6'

  const menuItemActiveStyle = 'bg-gray-100 text-gray-900 dark:bg-n-7 dark:text-white'
  const menuItemStyle = 'text-gray-700 dark:text-n-3'

  const iconStyle = 'mr-3 h-5 w-5 text-gray-400 dark:group-hover:text-gray-300'

  return (
    <Menu as="div" className="relative inline-block text-left">
      <div>
        <Menu.Button className={classNames("inline-flex w-full justify-center gap-x-1.5 rounded-md px-3 py-2 text-sm shadow-md", lightStylesMenu, darkStylesMenu)}>
          Actions
          <ChevronDownIcon className="-mr-1 h-5 w-5 text-gray-400" aria-hidden="true" />
        </Menu.Button>
      </div>

      <Transition
        as={Fragment}
        enter="transition ease-out duration-100"
        enterFrom="transform opacity-0 scale-95"
        enterTo="transform opacity-100 scale-100"
        leave="transition ease-in duration-75"
        leaveFrom="transform opacity-100 scale-100"
        leaveTo="transform opacity-0 scale-95"
      >
        <Menu.Items className="absolute right-0 z-10 mt-2 w-56 origin-top-right divide-y divide-gray-100 dark:divide-n-5 rounded-md bg-white dark:bg-black shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
          <div className="py-1">
            <Menu.Item>
              {({ active }) => (
                <Link
                  href="/connectors/google-drive"
                  className={classNames(
                    active ? menuItemActiveStyle : menuItemStyle,
                    'group flex items-center px-4 py-2 text-sm'
                  )}
                >
                  <DocumentPlusIcon
                    className={iconStyle}
                    aria-hidden="true"
                  />
                  Add Files
                </Link>
              )}
            </Menu.Item>
            {/* <Menu.Item>
              {({ active }) => (
                <Link
                  href="#"
                  className={classNames(
                    active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                    'group flex items-center px-4 py-2 text-sm'
                  )}
                >
                  <ArrowPathIcon
                    className="mr-3 h-5 w-5 text-gray-400 group-hover:text-gray-500"
                    aria-hidden="true"
                  />
                  Resync
                </Link>
              )}
            </Menu.Item> */}
          </div>
          <div className="py-1">
            <Menu.Item>
              {({ active }) => (
                <Link
                  href="#"
                  className={classNames(
                    active ? menuItemActiveStyle : menuItemStyle,
                    'group flex items-center px-4 py-2 text-sm'
                  )}
                >
                  <TrashIcon className={iconStyle} aria-hidden="true" />
                  Delete
                </Link>
              )}
            </Menu.Item>
          </div>
        </Menu.Items>
      </Transition>
    </Menu>
  )
}