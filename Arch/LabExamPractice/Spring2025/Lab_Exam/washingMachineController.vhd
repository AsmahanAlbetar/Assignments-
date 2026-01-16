library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity washingMachineController is

    port 
    (
        -- Inputs
        Clk   : in std_logic;
        reset : in std_logic;
        en    : in std_logic;

        -- Outputs
        fill_Led    : out std_logic;
        wash_Led    : out std_logic;
        rinse_Led   : out std_logic;
        spin_Led    : out std_logic
    );

end entity;

architecture arch_washingMachineController of washingMachineController is
-- Defining the states
type state is (fill, wash, rinse, spin);

begin

    process (Clk , reset)
    variable fillCounter  : integer := 0; -- 0 --> 3*20 - 1
    variable washCounter  : integer := 0; -- 0 --> 5*20 - 1
    variable rinseCounter : integer := 0; -- 0 --> 2*20 - 1
    variable spinCounter  : integer := 0; -- 0 --> 4*20 - 1
    variable myState      : state := fill;

    begin
        
        if (reset = '0') then
            -- reset logic
            fillCounter  := 0;
            washCounter  := 0;
            rinseCounter := 0;
            spinCounter  := 0;
            myState      := fill;
            fill_Led     <= '0';
            wash_Led     <= '0';
            rinse_Led    <= '0';
            spin_Led     <= '0';

        elsif (rising_edge(Clk)) and (en = '1') then
            -- main logic
            case myState is
                when fill =>

                    if (fillCounter < 59) then

                        fillCounter := fillCounter + 1;

                        fill_Led  <= '1';
                        wash_Led  <= '0';
                        rinse_Led <= '0';
                        spin_Led  <= '0';

                    else 
                        
                        fillCounter := 0;
                        myState := wash;

                    end if;

                when wash =>

                    if (washCounter < 99) then

                        washCounter := washCounter + 1;

                        fill_Led  <= '0';
                        wash_Led  <= '1';
                        rinse_Led <= '0';
                        spin_Led  <= '0';

                    else 
                        
                        washCounter := 0;
                        myState := rinse;

                    end if;

                when rinse =>

                    if (rinseCounter < 39) then

                        rinseCounter := rinseCounter + 1;

                        fill_Led  <= '0';
                        wash_Led  <= '0';
                        rinse_Led <= '1';
                        spin_Led  <= '0';

                    else 
                        
                        rinseCounter := 0;
                        myState := spin;

                    end if;

                when spin =>
                    
                    if (spinCounter < 79) then

                        spinCounter := spinCounter + 1;

                        fill_Led  <= '0';
                        wash_Led  <= '0';
                        rinse_Led <= '0';
                        spin_Led  <= '1';

                    else 
                        
                        spinCounter := 0;
                        myState := fill;

                    end if;
            
                when others =>
                    null;

            end case;

        end if;

    end process;

end architecture;