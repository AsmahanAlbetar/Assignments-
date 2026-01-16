library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;  

entity washingMachineController is
  port (
    Clk   : in std_logic;
    Reset : in std_logic; --Active low asynchronus reset
    en    : in std_logic; -- my clock enable 
    -- system outputs 
    fill_Led    : out std_logic;
    wash_Led    : out std_logic;
    rinse_Led  : out std_logic;
    spin_Led    : out std_logic

  ) ;
end washingMachineController ;

architecture arch_washingMachineController of washingMachineController is
  type state is (fill, wash, rinse, spin);
  signal my_state : state := fill;
  signal counter  : integer := 0;
begin
  process(Clk, Reset)
  begin
    if Reset = '0' then
      my_state <= fill;
      counter  <= 0;
      fill_Led <= '0';
      wash_Led <= '0';
      rinse_Led <= '0';
      spin_Led <= '0';
    elsif rising_edge(Clk) and en='1' then
      case my_state is
        when fill =>
          fill_Led  <= '1'; 
          wash_Led  <= '0'; 
          rinse_Led <= '0'; 
          spin_Led  <= '0';

          if counter < 59 then
            counter <= counter + 1;
          else
            counter <= 0;
            my_state <= wash;
          end if;
        when wash =>
          fill_Led  <= '0'; 
          wash_Led  <= '1'; 
          rinse_Led <= '0'; 
          spin_Led  <= '0';

          if counter < 99 then
            counter <= counter + 1;
          else
            counter <= 0;
            my_state <= rinse;
          end if;
        when rinse =>
          fill_Led  <= '0'; 
          wash_Led  <= '0'; 
          rinse_Led <= '1'; 
          spin_Led  <= '0';
          
          if counter < 39 then
            counter <= counter + 1;
          else
            counter <= 0;
            my_state <= spin;
          end if;
        when spin =>
          fill_Led <= '0'; wash_Led <= '0'; rinse_Led <= '0'; spin_Led <= '1';
          if counter < 79 then
            counter <= counter + 1;
          else
            counter <= 0;
            my_state <= fill;
          end if;
      end case;
    end if;
  end process;
end arch_washingMachineController;
